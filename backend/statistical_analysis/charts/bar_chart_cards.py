"""
bar_chart_cards.py — Bar chart: average number of cards (home vs away).
"""
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


def bar_chart_cards_global(df: pd.DataFrame):
    """Bar chart — average number of cards (home vs away)."""
    avg_yellow_home = df['HomeYellow'].mean().round(2)
    avg_yellow_away = df['AwayYellow'].mean().round(2)
    avg_red_home = df['HomeRed'].mean().round(2)
    avg_red_away = df['AwayRed'].mean().round(2)

    labels = [
        'Yellow (home)',
        'Yellow (away)',
        'Red (home)',
        'Red (away)'
    ]
    values = [avg_yellow_home, avg_yellow_away, avg_red_home, avg_red_away]
    colors = ['#ffcc00', '#ffcc00', '#ff3333', '#ff3333']
    edge_colors = ['#cc9900', '#cc9900', '#cc0000', '#cc0000']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        labels, values,
        color=colors,
        edgecolor=edge_colors,
        linewidth=1.5,
        width=0.6
    )

    for bar, val in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.02,
            f'{val}',
            ha='center', va='bottom',
            fontsize=12, fontweight='bold', color='black'
        )

    plt.title('Average number of cards per match by home and away',
              fontsize=16, pad=20, fontweight='bold')
    plt.ylabel('Average number of cards', fontsize=12)
    plt.ylim(0, max(values) * 1.3)
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    legend_elements = [
        Patch(facecolor='#ffcc00', edgecolor='#cc9900', label='Yellow card'),
        Patch(facecolor='#ff3333', edgecolor='#cc0000', label='Red card')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=11)

    plt.tight_layout()
    plt.show()
