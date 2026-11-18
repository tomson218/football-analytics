"""
visualisation_data.py — Data visualisations from MySQL data warehouse (football_dw).
Data comes from fact_matches table and dim_* dimensions in Star Schema model.

This file serves as the entry point — imports functions from charts/ submodules
and runs all charts in one loop.
"""
from .data_loaders import load_matches_df
from .charts import (
    pie_chart,
    bar_chart,
    bar_chart_cards_global,
    time_series_plot,
    goals_histogram,
    box_plot,
    violin_plot,
    scatter_plot,
)


# ============================================================
# Main function — runs all visualisations
# ============================================================

def visualizations_all():
    """Loads data from DB and generates all charts."""
    print("Loading data from MySQL database...")
    df = load_matches_df()
    print(f"Loaded {len(df)} matches.\n")

    print("1/9 — Pie chart (teams in leagues)...")
    pie_chart(df)

    print("2/9 — Bar chart (number of teams per league)...")
    bar_chart(df)

    print("3/9 — Bar chart (cards)...")
    bar_chart_cards_global(df)

    print("4/9 — Elo time series...")
    time_series_plot()

    print("5/9 — Home goals histogram...")
    goals_histogram(df, 'FTHome', 'home')

    print("6/9 — Away goals histogram...")
    goals_histogram(df, 'FTAway', 'away')

    print("7/9 — Elo box plot by league...")
    box_plot(df)

    print("8/9 — Fouls violin plot by league...")
    violin_plot(df)

    print("9/9 — Scatter plot (shots on target vs goals)...")
    scatter_plot(df)

    print("\nAll charts generated!")


if __name__ == '__main__':
    visualizations_all()
