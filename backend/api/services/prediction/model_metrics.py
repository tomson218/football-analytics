"""
prediction/model_metrics.py — Return model metrics from model_comparison.json.
Returns metrics for the 6-feature model used in production,
plus comparison data for all 3 models (Base, 10-Feature, 6-Feature).
"""
import json
from pathlib import Path
from typing import Dict, Any

RESULTS_PATH = Path(__file__).parent.parent.parent.parent / "ml_exploratory_analysis" / "results" / "model_comparison.json"


def _load_results() -> Dict[str, Any]:
    with open(RESULTS_PATH, "r") as f:
        return json.load(f)


def _rounded(metrics: Dict[str, float]) -> Dict[str, float]:
    return {name: round(value, 4) for name, value in metrics.items()}


def get_model_metrics() -> Dict[str, Any]:
    """
    Load and return key model metrics from model_comparison.json.
    Returns a simplified dict with test AUC, accuracy, F1 for the 6-feature model.
    """
    six = _load_results()["summary"]["six_feature_model"]
    return {
        "model_name": f"6-Feature ({six['features_count']} features)",
        "features_count": six["features_count"],
        "test_auc": round(six["test_auc"], 2),
        "test_accuracy": round(six["test_accuracy"], 2),
        "test_f1": round(six["test_f1"], 2),
    }


def get_all_models_comparison() -> Dict[str, Any]:
    """
    Return comparison data for all 3 models (Base 25, 10-Feature, 6-Feature).
    """
    data = _load_results()
    models = [
        {
            "model_name": res["model_name"],
            "features_count": res["features_count"],
            "features": res["features"],
            "validation_metrics": _rounded(res["validation_metrics"]),
            "test_metrics": _rounded(res["test_metrics"]),
            "feature_importance": {
                name: round(value, 2)
                for name, value in sorted(res["feature_importance"].items(), key=lambda x: x[1], reverse=True)
            },
        }
        for res in data["comparison"]
    ]
    return {"models": models, "summary": data["summary"]}
