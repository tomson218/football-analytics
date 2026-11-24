# API reference

The Football Analytics API is a FastAPI service that predicts **HomeNoLose**: the probability that the home team does not lose (home win or draw) from bookmaker odds and the Asian Handicap. Predictions use the 6-feature CatBoost model (`backend/ml_exploratory_analysis/models/catboost_6feat.cbm`).

- [Running the API](#running-the-api)
- [Endpoints](#endpoints)
- [Python functions](#python-functions)
- [Updating the documentation](#updating-the-documentation)

## Running the API

From the `backend` directory, with the requirements installed:

```bash
uvicorn api.main:app --port 8080 --reload
```

Or start the whole stack (MySQL, API and frontend) with `docker compose up -d` in the project root.

| URL | What it is |
|---|---|
| `http://localhost:8080/docs` | Interactive Swagger UI: every endpoint, with "Try it out" to send real requests |
| `http://localhost:8080/redoc` | The same documentation in ReDoc's read-only layout |
| `http://localhost:8080/openapi.json` | The OpenAPI specification |
| [`docs/api/index.html`](api/index.html) | A standalone copy of the Swagger UI that opens without the server. "Try it out" still needs the server running |

### Configuration

The API reads the project's root `.env` file.

| Variable | Used for | Default |
|---|---|---|
| `YOUR_HOST`, `YOUR_PORT`, `YOUR_USER`, `YOUR_PASSWORD`, `YOUR_DB_NAME` | MySQL connection for `/predict/data-stats` | — |
| `CORS_ORIGIN` | The frontend origin allowed to call the API | `http://localhost:5173` |

## Endpoints

All endpoints are under `/predict`. Any unexpected error, such as a missing model file or an unreachable database, returns **500** with the error message in `detail`.

| Method | Path | Returns | Needs MySQL |
|---|---|---|---|
| `POST` | [`/predict/home-no-lose`](#post-predicthome-no-lose) | Prediction for one match | No |
| `GET` | [`/predict/feature-importance`](#get-predictfeature-importance) | Importance of the 6 model features | No |
| `GET` | [`/predict/model-metrics`](#get-predictmodel-metrics) | Test metrics of the production model | No |
| `GET` | [`/predict/models-comparison`](#get-predictmodels-comparison) | Metrics and features of all 3 models | No |
| `GET` | [`/predict/data-stats`](#get-predictdata-stats) | Size of the data warehouse | Yes |

### `POST /predict/home-no-lose`

Predicts the probability that the home team does not lose, and compares it with the probability implied by the home odds.

**Request body**

| Field | Type | Range | Description |
|---|---|---|---|
| `odd_home` | float | 1.04–26.13 | Average opening odds for a home win |
| `odd_away` | float | 1.08–41.22 | Average opening odds for an away win |
| `max_home` | float | 1.06–35.0 | Best (maximum) opening odds for a home win across bookmakers |
| `max_draw` | float | 2.2–24.0 | Best opening odds for a draw |
| `max_away` | float | 1.1–65.0 | Best opening odds for an away win |
| `handi_size` | float | −3.5–2.8 | Asian Handicap, e.g. −0.5 means the home team gives half a goal |

The ranges are the minimum and maximum values seen in the training data. A missing field or a value outside its range returns **422** with the field name and the rule it broke.

**Response**

| Field | Type | Description |
|---|---|---|
| `probability` | float | Model probability that the home team does not lose, 0–1 |
| `implied_probability` | float | Probability implied by the home odds: `1 / odd_home` |
| `is_value_bet` | bool | `true` when `probability` is higher than `implied_probability` |

**Example**

```bash
curl -X POST http://localhost:8080/predict/home-no-lose \
  -H "Content-Type: application/json" \
  -d '{"odd_home": 1.85, "odd_away": 4.20, "max_home": 1.92, "max_draw": 3.60, "max_away": 4.40, "handi_size": -0.5}'
```

```json
{ "probability": 0.7412, "implied_probability": 0.5405, "is_value_bet": true }
```

The model gives the home team a 74.1% chance of not losing, while the home odds imply about 54%, so the match is flagged as a value bet. Note that `implied_probability` covers a home win only, whereas `probability` also includes the draw. The value-bet flag compares those two as the app does, so it should be read as a rough signal, not a betting recommendation.

### `GET /predict/feature-importance`

Returns how much each of the 6 model features contributes to predictions, as percentages that sum to 100. The frontend shows these next to the form fields.

```json
{ "odd_home": 25.5, "odd_away": 9.4, "max_away": 27.6, "handi_size": 7.8, "max_home": 11.7, "max_draw": 18.0 }
```

### `GET /predict/model-metrics`

Returns the test-set metrics of the production (6-feature) model, rounded to 2 decimals. The frontend shows the AUC in its header and footer.

```json
{ "model_name": "6-Feature (6 features)", "features_count": 6, "test_auc": 0.72, "test_accuracy": 0.71, "test_f1": 0.8 }
```

### `GET /predict/models-comparison`

Returns all 3 CatBoost models (base with 25 features, 10-feature and 6-feature), read from `ml_exploratory_analysis/results/model_comparison.json`.

- `models`: one entry per model, with its feature list, validation metrics (AUC, accuracy, precision, recall, log loss), test metrics (AUC, accuracy, F1, log loss) and feature importance sorted from highest to lowest.
- `summary`: the headline test metrics of each model, unrounded.

One entry of `models`:

```json
{
  "model_name": "6-Feature (top 6)",
  "features_count": 6,
  "features": ["OddHome", "OddAway", "MaxAway", "HandiSize", "MaxHome", "MaxDraw"],
  "validation_metrics": { "AUC": 0.7509, "Accuracy": 0.7285, "Precision": 0.7602, "Recall": 0.8814, "Logloss": 0.5353 },
  "test_metrics": { "AUC": 0.7158, "Accuracy": 0.7115, "F1": 0.8038, "Logloss": 0.5645 },
  "feature_importance": { "MaxAway": 27.56, "OddHome": 25.51, "MaxDraw": 18.03, "MaxHome": 11.7, "OddAway": 9.37, "HandiSize": 7.83 }
}
```

### `GET /predict/data-stats`

Counts the matches and leagues in the data warehouse and returns the season range. This is the only endpoint that queries MySQL.

```json
{ "total_matches": 8621, "total_leagues": 5, "season_start": "2020/21", "season_end": "2024/25" }
```

## Python functions

The API code is in `backend/api/`. Routers handle HTTP; services do the work and can be called from Python without the server.

```
api/
├── main.py                     # FastAPI app, CORS, router registration
├── export_docs.py              # Writes docs/api/ (OpenAPI spec + standalone Swagger UI)
├── models/                     # Request and response schemas (Pydantic)
├── routers/predict.py          # /predict/* endpoints
└── services/prediction/        # Model loading, prediction, metrics, warehouse stats
```

### `services/prediction/`

| Function | File | Description |
|---|---|---|
| `get_model()` | `load_model.py` | Loads `catboost_6feat.cbm` and returns the `CatBoostClassifier`. The model is loaded on the first call and cached for later calls. |
| `predict_home_no_lose(features)` | `predict.py` | Takes a dict with `OddHome`, `OddAway`, `MaxHome`, `MaxDraw`, `MaxAway` and `HandiSize`. Returns `probability`, `implied_probability` (`1 / OddHome`) and `is_value_bet`, rounded to 4 decimals. |
| `get_feature_importance()` | `feature_importance.py` | Returns the model's feature importance as percentages, with snake_case keys (`odd_home`, …). |
| `to_snake(name)` | `feature_importance.py` | Converts a CamelCase feature name to snake_case, e.g. `OddHome` → `odd_home`. |
| `get_model_metrics()` | `model_metrics.py` | Reads `model_comparison.json` and returns the 6-feature model's test AUC, accuracy and F1, rounded to 2 decimals. |
| `get_all_models_comparison()` | `model_metrics.py` | Reads `model_comparison.json` and returns all 3 models with their metrics (4 decimals) and feature importance, plus the summary. |
| `get_data_stats()` | `data_stats.py` | Queries `fact_matches` joined with `dim_division` and `dim_date`, and returns the match count, league count, and first and last season. |

The model stores its features by position (`0`–`5`), not by name. `predict_home_no_lose()` and `get_feature_importance()` rely on `FEATURE_COLS_6` in `backend/common/constants.py` listing the features in the order the model was trained with. Don't reorder that list without retraining the model.

Example, calling a service directly from the `backend` directory:

```python
from api.services.prediction.predict import predict_home_no_lose

predict_home_no_lose({
    "OddHome": 1.85, "OddAway": 4.20, "MaxHome": 1.92,
    "MaxDraw": 3.60, "MaxAway": 4.40, "HandiSize": -0.5,
})
# {'probability': 0.7412, 'implied_probability': 0.5405, 'is_value_bet': True}
```

### `models/`

| Class | File | Description |
|---|---|---|
| `OddsPredictionRequest` | `odds_prediction_request.py` | Body of `POST /predict/home-no-lose`. Validates each field's range and supplies the example shown in Swagger. |
| `OddsPredictionResponse` | `odds_prediction_response.py` | Response of `POST /predict/home-no-lose`. |

### `routers/predict.py`

| Function | Description |
|---|---|
| One function per endpoint | Calls the matching service. The function's docstring becomes the endpoint description in Swagger. |
| `errors_as_http_500(endpoint)` | Decorator that turns any exception into an HTTP 500 response with the error message. |
| `example(body)` | Builds the example response that Swagger shows for an endpoint. |

## Updating the documentation

Swagger at `/docs` is generated from the code, so it updates whenever the API changes:

- **Endpoint description**: the endpoint function's docstring.
- **Short title**: `summary=` in the route decorator.
- **Field descriptions and ranges**: `Field(...)` in the Pydantic models.
- **Example responses**: `responses=example({...})` in the route decorator.

After changing the API, regenerate the files in `docs/api/` from the `backend` directory:

```bash
python -m api.export_docs
```

Then update this page if an endpoint, field or function was added, removed or changed.
