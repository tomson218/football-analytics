"""
bar_chart.py — Bar chart: number of teams in each league.
"""
import matplotlib.pyplot as plt
import pandas as pd

from .league_data import teams_per_league


def bar_chart(df: pd.DataFrame):
    """Bar chart — number of teams in each league."""
    labels, counts = teams_per_league(df)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, counts, color=['#9467bd', '#1f77b4', '#2ca02c', '#d62728', '#ff7f0e'])

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.3,
                 f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title("Number of teams in each league in seasons 2022–2025", fontsize=16, pad=20)
    plt.ylabel("Number of teams", fontsize=12)
    plt.xlabel("League", fontsize=12)
    plt.ylim(0, max(counts) * 1.15)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.show()
