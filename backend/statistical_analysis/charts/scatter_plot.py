"""
scatter_plot.py — Scatter plot + linear regression: shots on target vs goals.
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

SIDES = [
    ('home', 'HomeTarget', 'FTHome', 'blue'),
    ('away', 'AwayTarget', 'FTAway', 'green'),
]


def scatter_plot(df: pd.DataFrame):
    """Scatter plot + linear regression (shots on target vs goals)."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    coefficients = []

    for ax, (side, target_col, goals_col, color) in zip(axes, SIDES):
        X = df[target_col].values.reshape(-1, 1)
        Y = df[goals_col].values
        model = LinearRegression().fit(X, Y)
        a, b = model.coef_[0], model.intercept_
        coefficients.append((a, b))

        ax.scatter(X, Y, color=color, alpha=0.6, label='Data')
        ax.plot(X, model.predict(X), color='red', label=f'y = {a:.2f}x + {b:.2f}')
        ax.set_title(f"Regression: Shots on target vs goals scored by {side} team")
        ax.set_xlabel(f"{side.capitalize()} shots on target")
        ax.set_ylabel(f"{side.capitalize()} goals scored")
        ax.legend()

    plt.tight_layout()
    plt.show()

    return tuple(coefficients)
