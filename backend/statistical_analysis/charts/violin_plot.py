"""
violin_plot.py — Violin plot: fouls by league.
"""
import matplotlib.pyplot as plt
import pandas as pd

from .league_data import home_away_values_per_league


def violin_plot(df: pd.DataFrame):
    """Violin plot — fouls by league."""
    labels, all_fouls_data = home_away_values_per_league(df, 'HomeFouls', 'AwayFouls')

    plt.figure(figsize=(12, 6))
    plt.violinplot(all_fouls_data, showmeans=True, showmedians=True)

    plt.xticks(range(1, len(labels) + 1), labels, rotation=45)
    plt.xlabel("League")
    plt.ylabel("Fouls")
    plt.title("Fouls distribution by league")
    plt.tight_layout()
    plt.show()
