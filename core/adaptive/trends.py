"""Deterministic local unit-trend queries over completed score reports."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from core.db.models import Role, TrainingSessionRecord, User
from core.db.security import require_role


@dataclass(frozen=True)
class TrendPoint:
    """Aggregate score data for one local selection mode."""

    selection_mode: str
    completed_sessions: int
    average_score: float
    rating_eligible_sessions: int


def unit_trends(
    *,
    session_factory: sessionmaker[Session],
    actor_id: str,
) -> tuple[TrendPoint, ...]:
    """Return aggregate local trends without outbound analytics or telemetry."""
    with session_factory() as db:
        require_role(db.get(User, actor_id), [Role.INSTRUCTOR, Role.ADMIN])
        rows = db.scalars(
            select(TrainingSessionRecord)
            .where(TrainingSessionRecord.score_json.is_not(None))
            .order_by(TrainingSessionRecord.selection_mode, TrainingSessionRecord.session_id)
        )
        totals: dict[str, list[float]] = defaultdict(list)
        eligible: dict[str, int] = defaultdict(int)
        for row in rows:
            score = json.loads(row.score_json or "{}")
            totals[row.selection_mode].append(float(score.get("total_score", 0.0)))
            if row.rating_eligible:
                eligible[row.selection_mode] += 1

    return tuple(
        TrendPoint(
            selection_mode=mode,
            completed_sessions=len(scores),
            average_score=round(sum(scores) / len(scores), 6),
            rating_eligible_sessions=eligible[mode],
        )
        for mode, scores in sorted(totals.items())
    )
