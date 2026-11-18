"""
pie_chart.py — Pie chart: percentage of teams in leagues.
"""
import matplotlib.pyplot as plt
import pandas as pd

from .league_data import teams_per_league


def pie_chart(df: pd.DataFrame):
    """Pie chart — percentage of teams in each league."""
    labels, counts = teams_per_league(df)

    plt.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.title("Percentage of teams in each league across seasons 2022/2025")
    plt.show()
