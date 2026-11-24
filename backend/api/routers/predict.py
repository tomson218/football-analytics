"""
routers/predict.py — /predict/* endpoints.
Feature importance and HomeNoLose prediction using the trained CatBoost model.
"""
from functools import wraps

from fastapi import APIRouter, HTTPException

from ..models import OddsPredictionRequest, OddsPredictionResponse
from ..services.prediction.data_stats import get_data_stats as _get_data_stats
from ..services.prediction.feature_importance import get_feature_importance as _get_feature_importance
from ..services.prediction.model_metrics import get_model_metrics as _get_model_metrics
from ..services.prediction.model_metrics import get_all_models_comparison as _get_all_models_comparison
from ..services.prediction.predict import predict_home_no_lose as _predict_home_no_lose

router = APIRouter(prefix="/predict", tags=["predict"])

SERVER_ERROR = {500: {"description": "Unexpected error, e.g. the model file or the database is unavailable."}}


def example(body, extra=None):
    """Build an OpenAPI `responses` entry with an example 200 body, for Swagger."""
    return {200: {"content": {"application/json": {"example": body}}}, **SERVER_ERROR, **(extra or {})}


def errors_as_http_500(endpoint):
    """Report unexpected endpoint errors as HTTP 500 with the error message."""
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        try:
            return endpoint(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper


@router.get(
    "/feature-importance",
    summary="Feature importance of the production model",
    responses=example({
        "odd_home": 25.5, "odd_away": 9.4, "max_away": 27.6,
        "handi_size": 7.8, "max_home": 11.7, "max_draw": 18.0,
    }),
)
@errors_as_http_500
def get_feature_importance():
    """
    Return the feature importance percentages for the 6 features
    used in the production model (HomeNoLose prediction).
    All 6 features are provided by the user: 5 odds and the Asian Handicap (HandiSize).
    """
    return _get_feature_importance()


@router.get(
    "/model-metrics",
    summary="Test metrics of the production model",
    responses=example({
        "model_name": "6-Feature (6 features)", "features_count": 6,
        "test_auc": 0.72, "test_accuracy": 0.71, "test_f1": 0.8,
    }),
)
@errors_as_http_500
def get_model_metrics():
    """
    Return the API model metrics (AUC, accuracy, F1)
    loaded from model_comparison.json.
    """
    return _get_model_metrics()


@router.get(
    "/models-comparison",
    summary="Compare the 3 CatBoost models",
    responses=example({
        "models": [{
            "model_name": "6-Feature (top 6)",
            "features_count": 6,
            "features": ["OddHome", "OddAway", "MaxAway", "HandiSize", "MaxHome", "MaxDraw"],
            "validation_metrics": {"AUC": 0.7509, "Accuracy": 0.7285, "Precision": 0.7602, "Recall": 0.8814, "Logloss": 0.5353},
            "test_metrics": {"AUC": 0.7158, "Accuracy": 0.7115, "F1": 0.8038, "Logloss": 0.5645},
            "feature_importance": {"MaxAway": 27.56, "OddHome": 25.51, "MaxDraw": 18.03, "MaxHome": 11.7, "OddAway": 9.37, "HandiSize": 7.83},
        }],
        "summary": {
            "six_feature_model": {
                "features_count": 6,
                "features": ["OddHome", "OddAway", "MaxAway", "HandiSize", "MaxHome", "MaxDraw"],
                "test_auc": 0.7158, "test_accuracy": 0.7115, "test_f1": 0.8038,
            },
        },
    }),
)
@errors_as_http_500
def get_models_comparison():
    """
    Return comparison data for all 3 CatBoost models:
    - Base (25 features): full model with all features
    - 10-Feature: top 10 features by importance
    - 6-Feature: top 6 features by importance (used in production)

    Each model includes validation metrics, test metrics, and feature importance.
    """
    return _get_all_models_comparison()


@router.post(
    "/home-no-lose",
    response_model=OddsPredictionResponse,
    summary="Predict whether the home team avoids defeat",
    responses={**SERVER_ERROR, 422: {"description": "A field is missing or outside its allowed range."}},
)
@errors_as_http_500
def predict_home_no_lose(request: OddsPredictionRequest):
    """
    Predict the probability that the home team will not lose (win or draw)
    based on betting odds using the trained CatBoost model (6-feature model).
    Uses 5 odds and the Asian Handicap (HandiSize) provided by the user.
    """
    odds = {
        'OddHome': request.odd_home,
        'OddAway': request.odd_away,
        'MaxHome': request.max_home,
        'MaxDraw': request.max_draw,
        'MaxAway': request.max_away,
        'HandiSize': request.handi_size,
    }
    return OddsPredictionResponse(**_predict_home_no_lose(odds))


@router.get(
    "/data-stats",
    summary="Size of the data warehouse",
    responses=example({
        "total_matches": 8621, "total_leagues": 5,
        "season_start": "2020/21", "season_end": "2024/25",
    }),
)
@errors_as_http_500
def get_data_stats():
    """
    Return dynamic dataset statistics from the data warehouse:
    total matches, total leagues, and season range.
    """
    return _get_data_stats()
