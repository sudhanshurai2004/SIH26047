"""Pure, deterministic scoring of trainee events against an abstract doctrine."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from typing import Any

from core.contracts import ContractValidationError, validate_payload
from core.scoring.doctrine import DoctrineValidationError, validate_doctrine


class ScoringError(ValueError):
    """Raised when score inputs cannot be safely evaluated."""


@dataclass(frozen=True)
class NodeResult:
    """Auditable result for one doctrine decision-tree node."""

    node_id: str
    action: str
    skill_tags: tuple[str, ...]
    outcome: str
    event_id: str | None
    target_id: str | None
    detection_delay_ms: int | None
    timing_band: str | None
    max_points: float
    points: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoreReport:
    """Serializable result of a complete decision-tree traversal."""

    scenario_id: str
    doctrine_id: str
    doctrine_version: str
    max_score: int
    total_score: float
    interrupted: bool
    rating_eligible: bool
    node_results: tuple[NodeResult, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "doctrine_id": self.doctrine_id,
            "doctrine_version": self.doctrine_version,
            "max_score": self.max_score,
            "total_score": self.total_score,
            "interrupted": self.interrupted,
            "rating_eligible": self.rating_eligible,
            "node_results": [result.as_dict() for result in self.node_results],
        }


def score_scenario(
    scenario: Mapping[str, Any],
    events: Iterable[Mapping[str, Any]],
    doctrine: Mapping[str, Any],
    *,
    interrupted: bool = False,
) -> ScoreReport:
    """Score events with no wall-clock input and no hidden scoring weights.

    Every action contribution is ``doctrine.max_score * doctrine.weight``.
    Detection credit is computed only from doctrine timing thresholds and the
    target's precomputed ``t_visible_ms`` marker, never scenario start time.
    """
    event_list = [dict(event) for event in events]
    _validate_inputs(scenario, event_list, doctrine)
    sorted_events = sorted(
        event_list,
        key=lambda event: (event["sequence"], event["t_offset_ms"], event["event_id"]),
    )
    interruption_sequences = [
        event["sequence"] for event in sorted_events if event["event_type"] == "session_interrupted"
    ]
    is_interrupted = interrupted or bool(interruption_sequences)
    if interruption_sequences:
        first_interruption = min(interruption_sequences)
        sorted_events = [event for event in sorted_events if event["sequence"] < first_interruption]

    targets = {target["target_id"]: target for target in scenario["targets"]}
    nodes = {node["node_id"]: node for node in doctrine["decision_tree"]["nodes"]}
    weights = doctrine["scoring"]["weights"]
    max_score = int(doctrine["scoring"]["max_score"])
    allowed_responses = set(doctrine["roe"]["allowed_responses"])

    node_results: list[NodeResult] = []
    current_node_id: str | None = doctrine["decision_tree"]["root_node_id"]
    previous_sequence = -1
    visited: set[str] = set()

    while current_node_id is not None:
        if current_node_id in visited:
            # validate_doctrine rejects cycles. This is a defensive guard for a
            # mutated in-memory mapping supplied by a caller after validation.
            raise ScoringError("doctrine traversal encountered a cycle")
        visited.add(current_node_id)
        node = nodes[current_node_id]
        action = node["action"]
        event = _next_event(sorted_events, action, previous_sequence)
        max_points = round(max_score * float(weights[action]), 6)

        if event is None:
            result = NodeResult(
                node_id=node["node_id"],
                action=action,
                skill_tags=tuple(node["skill_tags"]),
                outcome="timeout",
                event_id=None,
                target_id=None,
                detection_delay_ms=None,
                timing_band=None,
                max_points=max_points,
                points=0.0,
            )
            branch = "timeout"
        else:
            previous_sequence = int(event["sequence"])
            result, branch = _score_event(
                node=node,
                event=event,
                targets=targets,
                doctrine=doctrine,
                allowed_responses=allowed_responses,
                max_points=max_points,
            )

        node_results.append(result)
        current_node_id = node["branches"][branch]

    total_score = round(sum(result.points for result in node_results), 6)
    return ScoreReport(
        scenario_id=str(scenario["scenario_id"]),
        doctrine_id=str(doctrine["doctrine_id"]),
        doctrine_version=str(doctrine["version"]),
        max_score=max_score,
        total_score=total_score,
        interrupted=is_interrupted,
        rating_eligible=not is_interrupted,
        node_results=tuple(node_results),
    )


def _validate_inputs(
    scenario: Mapping[str, Any],
    events: Iterable[Mapping[str, Any]],
    doctrine: Mapping[str, Any],
) -> None:
    """Validate untrusted contract-shaped values before indexing their fields."""
    try:
        validate_payload("scenario", scenario)
        validate_doctrine(doctrine)
        for event in events:
            validate_payload("event", event)
            if event["scenario_id"] != scenario["scenario_id"]:
                raise ScoringError("event scenario_id does not match the scored scenario")
            if event["t_offset_ms"] > scenario["duration_ms"]:
                raise ScoringError("event t_offset_ms exceeds scenario duration")
    except (ContractValidationError, DoctrineValidationError) as error:
        raise ScoringError(str(error)) from error


def _next_event(
    events: list[dict[str, Any]], action: str, previous_sequence: int
) -> dict[str, Any] | None:
    """Use the first matching trainee action after the preceding tree action."""
    for event in events:
        if event["event_type"] == action and event["sequence"] > previous_sequence:
            return event
    return None


def _score_event(
    *,
    node: Mapping[str, Any],
    event: Mapping[str, Any],
    targets: Mapping[str, Mapping[str, Any]],
    doctrine: Mapping[str, Any],
    allowed_responses: set[str],
    max_points: float,
) -> tuple[NodeResult, str]:
    """Score one event and return the result plus its decision-tree branch."""
    action = str(node["action"])
    payload = event["payload"]
    target_id = str(payload.get("target_id")) if "target_id" in payload else None
    event_value = _event_value(action, payload)
    correct = event_value in node["expected_values"]
    detection_delay_ms: int | None = None
    timing_band: str | None = None
    credit = 1.0

    if action == "detect":
        target = targets.get(target_id or "")
        if target is None:
            correct = False
            timing_band = "unknown_target"
            credit = 0.0
        else:
            detection_delay_ms = int(event["t_offset_ms"]) - int(target["t_visible_ms"])
            timing_band, credit = _detection_credit(
                detection_delay_ms,
                doctrine["scoring"]["detection_delay"],
            )
            if detection_delay_ms < 0:
                correct = False

    if action == "respond" and event_value not in allowed_responses:
        correct = False

    points = round(max_points * credit, 6) if correct else 0.0
    outcome = "correct" if correct else "incorrect"
    return (
        NodeResult(
            node_id=str(node["node_id"]),
            action=action,
            skill_tags=tuple(node["skill_tags"]),
            outcome=outcome,
            event_id=str(event["event_id"]),
            target_id=target_id,
            detection_delay_ms=detection_delay_ms,
            timing_band=timing_band,
            max_points=max_points,
            points=points,
        ),
        outcome,
    )


def _event_value(action: str, payload: Mapping[str, Any]) -> str:
    """Extract the abstract value compared with the doctrine's expected values."""
    if action == "detect":
        return "detected"
    value_key = {
        "classify": "classification",
        "assess": "assessment",
        "respond": "response",
    }[action]
    return str(payload[value_key])


def _detection_credit(delay_ms: int, thresholds: Mapping[str, Any]) -> tuple[str, float]:
    """Return a threshold-only timing band and continuous credit.

    The frozen v1 doctrine exposes timing thresholds but no additional scoring
    coefficients. To avoid inventing another weight, credit falls linearly from
    1.0 at ``excellent_ms`` to 0.0 at ``late_ms``. ``acceptable_ms`` remains an
    auditable band boundary in the AAR result.
    """
    excellent_ms = int(thresholds["excellent_ms"])
    acceptable_ms = int(thresholds["acceptable_ms"])
    late_ms = int(thresholds["late_ms"])
    if delay_ms < 0:
        return "before_visible", 0.0
    if delay_ms <= excellent_ms:
        return "excellent", 1.0
    if delay_ms <= acceptable_ms:
        band = "acceptable"
    elif delay_ms <= late_ms:
        band = "late"
    else:
        return "missed", 0.0

    # Doctrine validation ensures late_ms > excellent_ms.
    credit = (late_ms - delay_ms) / (late_ms - excellent_ms)
    return band, round(max(0.0, min(1.0, credit)), 6)
