"""Weakness-targeted selection, per-skill ratings, and local unit trends."""

from core.adaptive.elo import (
    DEFAULT_RATING,
    ScenarioOption,
    SkillModel,
    SkillUpdate,
    select_next_scenario,
)
from core.adaptive.trends import TrendPoint, unit_trends

__all__ = [
    "DEFAULT_RATING",
    "ScenarioOption",
    "SkillModel",
    "SkillUpdate",
    "TrendPoint",
    "select_next_scenario",
    "unit_trends",
]
