"""Validated loading and semantic checks for abstract training doctrine."""

from __future__ import annotations

from collections.abc import Mapping
from math import isclose
from pathlib import Path
from typing import Any

from core.contracts import ContractValidationError, load_and_validate, validate_payload


class DoctrineValidationError(ValueError):
    """Raised when a doctrine is structurally valid but not executable."""


def load_doctrine(path: Path) -> dict[str, Any]:
    """Safely load a local YAML doctrine and check its executable semantics."""
    try:
        doctrine = load_and_validate("doctrine", path)
    except ContractValidationError as error:
        raise DoctrineValidationError(str(error)) from error
    if not isinstance(doctrine, dict):
        raise DoctrineValidationError("doctrine root must be an object")
    validate_doctrine(doctrine)
    return doctrine


def validate_doctrine(doctrine: Mapping[str, Any]) -> None:
    """Validate the frozen schema plus the decision-tree invariants it cannot express."""
    try:
        validate_payload("doctrine", doctrine)
    except ContractValidationError as error:
        raise DoctrineValidationError(str(error)) from error

    errors: list[str] = []
    weights = doctrine["scoring"]["weights"]
    if not isclose(sum(float(value) for value in weights.values()), 1.0, abs_tol=1e-9):
        errors.append("scoring weights must sum to 1.0")

    delay = doctrine["scoring"]["detection_delay"]
    if not (delay["excellent_ms"] <= delay["acceptable_ms"] <= delay["late_ms"]):
        errors.append("detection-delay thresholds must be ordered excellent <= acceptable <= late")
    if delay["excellent_ms"] == delay["late_ms"]:
        errors.append("excellent_ms and late_ms must not be equal")

    tree = doctrine["decision_tree"]
    nodes = tree["nodes"]
    node_ids = [node["node_id"] for node in nodes]
    known_ids = set(node_ids)
    if len(known_ids) != len(node_ids):
        errors.append("decision-tree node_id values must be unique")
    if tree["root_node_id"] not in known_ids:
        errors.append("decision-tree root_node_id must refer to a node")

    allowed_responses = set(doctrine["roe"]["allowed_responses"])
    for node in nodes:
        for branch_id in node["branches"].values():
            if branch_id is not None and branch_id not in known_ids:
                errors.append(
                    f"node '{node['node_id']}' has an unknown branch target '{branch_id}'"
                )
        if node["action"] == "respond" and not set(node["expected_values"]).issubset(
            allowed_responses
        ):
            errors.append(
                f"respond node '{node['node_id']}' expects a response outside the doctrine ROE"
            )

    if not errors:
        _assert_acyclic_tree(tree["root_node_id"], nodes)
    if errors:
        raise DoctrineValidationError("; ".join(errors))


def _assert_acyclic_tree(root_node_id: str, nodes: list[Mapping[str, Any]]) -> None:
    """Reject loops so a malformed editable doctrine cannot score indefinitely."""
    by_id = {node["node_id"]: node for node in nodes}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise DoctrineValidationError("decision tree must not contain a cycle")
        if node_id in visited:
            return
        visiting.add(node_id)
        for child_id in by_id[node_id]["branches"].values():
            if child_id is not None:
                visit(child_id)
        visiting.remove(node_id)
        visited.add(node_id)

    visit(root_node_id)
