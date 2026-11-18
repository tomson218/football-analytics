"""
run_odds_stats.py — Entry point for odds statistics.
"""
from ..data_loaders import load_matches_df
from .odds_distribution import odds_distribution
from .implied_probability import odds_implied_probability


def run_odds_stats():
    """Loads data from DB and prints odds statistics."""
    print("Loading data from MySQL database...")
    df = load_matches_df()
    print(f"Loaded {len(df)} matches.\n")

    dist = odds_distribution(df)
    print("=== ODDS DISTRIBUTION ===")
    print(dist.round(4))
    print()

    implied = odds_implied_probability(df)
    print("=== IMPLIED PROBABILITY ===")
    print(implied.round(4))

    return dist, implied


if __name__ == '__main__':
    run_odds_stats()
