"""
load_model.py — Load the CatBoost model.
Uses the 6-feature model — top 6 features by importance from the base model.

CatBoost works with raw data — no scaler is needed.
"""
import os
from functools import lru_cache

import catboost

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, '..', '..', '..', 'ml_exploratory_analysis', 'models', 'catboost_6feat.cbm')


@lru_cache(maxsize=1)
def get_model() -> catboost.CatBoostClassifier:
    """Get the CatBoost model (6-feature), loaded on first call."""
    model = catboost.CatBoostClassifier()
    model.load_model(model_path)
    return model
