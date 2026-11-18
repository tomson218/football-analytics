"""
tables/__init__.py — Collects all data warehouse table definitions.

Organised by table type:
1. Raw staging tables (raw/)
2. Dimension tables (dim/)
3. Fact tables (fact/)
"""
from .raw import raw_elo_ratings_sql, raw_matches_sql
from .dim import (
    dim_country_sql,
    dim_division_sql,
    dim_team_sql,
    dim_season_sql,
    dim_date_sql,
)
from .fact import fact_matches_sql

TABLES = [
    raw_elo_ratings_sql,
    raw_matches_sql,
    dim_country_sql,
    dim_division_sql,
    dim_team_sql,
    dim_season_sql,
    dim_date_sql,
    fact_matches_sql,
]
