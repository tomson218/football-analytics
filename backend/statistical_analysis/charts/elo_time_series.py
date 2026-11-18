"""
elo_time_series.py — Elo time series for top 5 teams.
"""
import matplotlib.pyplot as plt
import pandas as pd

from ..data_loaders import load_elo_timeseries_df


def time_series_plot():
    """Elo time series for top 5 teams."""
    clubs_to_compare = ['Real Madrid', 'Ajax', 'Bayern Munich', 'Inter', 'Paris SG']

    elo_df = load_elo_timeseries_df()
    club_data = elo_df[elo_df['club'].isin(clubs_to_compare)]
    club_data = club_data.sort_values(['club', 'MatchDate'])

    plt.figure(figsize=(14, 8))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    color_map = dict(zip(clubs_to_compare, colors))

    for club in clubs_to_compare:
        data = club_data[club_data['club'] == club]
        plt.plot(
            data['MatchDate'], data['elo'],
            label=club,
            color=color_map[club],
            markersize=6,
            linewidth=2,
            linestyle='-',
            alpha=0.9
        )

    plt.title('Elo time series for top 5 teams from each league',
              fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Elo Rating', fontsize=12)
    plt.grid(alpha=0.3, linestyle='--', linewidth=0.7)
    plt.legend(
        title='Club',
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        fontsize=11,
        frameon=True,
        fancybox=True,
        shadow=True
    )
    plt.tight_layout()
    plt.show()
