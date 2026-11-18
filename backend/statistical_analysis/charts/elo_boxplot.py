"""
elo_boxplot.py — Box plot: Elo distribution by league.
"""
import matplotlib.pyplot as plt
import pandas as pd

from .league_data import home_away_values_per_league


def box_plot(df: pd.DataFrame):
    """Box plot — Elo rating distribution by league."""
    labels, all_elo_ratings_data = home_away_values_per_league(df, 'HomeElo', 'AwayElo')

    plt.figure(figsize=(12, 6))
    plt.boxplot(all_elo_ratings_data, patch_artist=True,
                boxprops=dict(facecolor='lightblue'), medianprops=dict(color='blue'))

    plt.xticks(range(1, len(labels) + 1), labels, rotation=45)
    plt.xlabel("League")
    plt.ylabel("Elo Rating")
    plt.title("Elo rating distribution by league")
    plt.tight_layout()
    plt.show()
