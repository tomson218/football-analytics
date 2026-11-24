from pydantic import BaseModel, Field


class OddsPredictionRequest(BaseModel):
    """
    Request body for HomeNoLose prediction.

    The 5 odds fields represent bookmaker odds for a football match:
    - `odd_*` — the average opening odds from multiple bookmakers.
    - `max_*` — the maximum (best) odds found across all bookmakers.

    HandiSize is the Asian Handicap value, typically between -3.5 and 2.8.
    """
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "odd_home": 1.85,
                    "odd_away": 4.20,
                    "max_home": 1.92,
                    "max_draw": 3.60,
                    "max_away": 4.40,
                    "handi_size": -0.5,
                }
            ]
        }
    }

    odd_home: float = Field(
        ...,
        ge=1.04, le=26.13,
        description="Average opening odds for the home team to win. The consensus price across bookmakers at the start of the match (e.g. 1.85). Range: 1.04–26.13."
    )
    odd_away: float = Field(
        ...,
        ge=1.08, le=41.22,
        description="Average opening odds for the away team to win. The consensus bookmaker price for the away team winning (e.g. 4.20). Range: 1.08–41.22."
    )
    max_home: float = Field(
        ...,
        ge=1.06, le=35.0,
        description="Maximum (best) opening odds for the home team to win. The highest price offered by any single bookmaker (e.g. 1.90). Range: 1.06–35.0."
    )
    max_draw: float = Field(
        ...,
        ge=2.2, le=24.0,
        description="Maximum (best) opening odds for a draw. The highest draw price offered by any single bookmaker (e.g. 3.50). Range: 2.2–24.0."
    )
    max_away: float = Field(
        ...,
        ge=1.1, le=65.0,
        description="Maximum (best) opening odds for the away team to win. The highest away-win price offered by any single bookmaker (e.g. 4.30). Range: 1.1–65.0."
    )
    handi_size: float = Field(
        ...,
        ge=-3.5, le=2.8,
        description="Asian Handicap value. Represents the goal handicap for the match (e.g. -0.3 means home team gives 0.3 goals)."
    )
