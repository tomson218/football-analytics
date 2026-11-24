from typing import Optional
from pydantic import BaseModel, Field


class OddsPredictionResponse(BaseModel):
    """Response from HomeNoLose prediction."""
    probability: float = Field(
        ...,
        description="Model probability that the home team does not lose (win or draw), from 0 to 1.",
        examples=[0.7412],
    )
    implied_probability: float = Field(
        ...,
        description="Probability implied by the average home odds: 1 / odd_home.",
        examples=[0.5405],
    )
    is_value_bet: Optional[bool] = Field(
        None,
        description="True when the model probability is higher than the implied probability.",
        examples=[True],
    )
