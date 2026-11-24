"""
feature_importance.py — Get feature importance percentages for the 6-feature model.
Returns importance for all 6 features used in the production model.
"""
import re
from typing import Dict

from common.constants import FEATURE_COLS_6
from .load_model import get_model


def to_snake(name: str) -> str:
    """Convert a CamelCase feature name to snake_case."""
    return re.sub(r'(?<!^)([A-Z])', r'_\1', name).lower()


def get_feature_importance() -> Dict[str, float]:
    """
    Return feature importance percentages for the 6 features
    used in the production model (HomeNoLose prediction).
    All 6 features are provided by the user: 5 odds and the Asian Handicap (HandiSize).
    """
    importance = get_model().get_feature_importance()
    total = importance.sum()
    return {
        to_snake(col): round(float(value) / total * 100, 1)
        for col, value in zip(FEATURE_COLS_6, importance)
    }
