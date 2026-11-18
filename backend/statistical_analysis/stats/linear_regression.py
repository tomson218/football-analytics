"""
linear_regression.py — Linear regression: shots on target vs goals.
Combines home and away data.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def linear_regression(df: pd.DataFrame):
    """
    Simple linear regression: shots on target (X) vs goals (Y).
    Combines home and away data.
    Returns coefficients (a, b) where Y = a*X + b.
    """
    X = np.concatenate([
        df["HomeTarget"].values,
        df["AwayTarget"].values
    ]).reshape(-1, 1)

    Y = np.concatenate([
        df["FTHome"].values,
        df["FTAway"].values
    ])

    model = LinearRegression()
    model.fit(X, Y)

    a = model.coef_[0]
    b = model.intercept_

    return a, b
