"""
goals_histogram.py — Histogram: goals scored by the home or away team.
"""
import matplotlib.pyplot as plt
import pandas as pd


def goals_histogram(df: pd.DataFrame, goals_col: str, side: str):
    """Histogram — goals scored by the given side ('home' or 'away')."""
    goals = df[goals_col].dropna().astype(int)

    plt.figure(figsize=(11, 6))
    plt.hist(
        goals,
        bins=range(0, goals.max() + 2),
        color='#2E86AB',
        edgecolor='black',
        alpha=0.8
    )

    plt.title(f"Histogram of goals scored by {side} team", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Number of goals", fontsize=12)
    plt.ylabel("Number of matches", fontsize=12)

    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(range(0, goals.max() + 1))
    plt.tight_layout()
    plt.show()
