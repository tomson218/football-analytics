"""
predict.py — Predict the probability that the home team will not lose.
Uses the 6-feature model — 5 bookmaker odds + the Asian Handicap (HandiSize).
CatBoost works with raw data — no scaler is needed.
"""
import pandas as pd
from typing import Dict, Any

from common.constants import FEATURE_COLS_6
from .load_model import get_model


def predict_home_no_lose(features: Dict[str, float]) -> Dict[str, Any]:
    """
    Predict the probability that the home team will not lose.

    Args:
        features: Dictionary with the 6 model features:
            OddHome, OddAway, MaxHome, MaxDraw, MaxAway, HandiSize

    Returns:
        Dictionary with: probability (float), implied_probability (float), is_value_bet (bool)
    """
    X = pd.DataFrame([features], columns=FEATURE_COLS_6)
    proba = float(get_model().predict_proba(X)[0][1])  # P(HomeNoLose)

    # Implied probability from OddHome (the API guarantees OddHome >= 1.04)
    implied_prob = 1.0 / features['OddHome']

    return {
        'probability': round(proba, 4),
        'implied_probability': round(implied_prob, 4),
        'is_value_bet': proba > implied_prob,
    }
