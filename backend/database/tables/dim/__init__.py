"""
tables/dim/__init__.py — Re-exports dimension table definitions.
"""
from .dim_country import SQL as dim_country_sql
from .dim_division import SQL as dim_division_sql
from .dim_team import SQL as dim_team_sql
from .dim_season import SQL as dim_season_sql
from .dim_date import SQL as dim_date_sql

__all__ = [
    'dim_country_sql',
    'dim_division_sql',
    'dim_team_sql',
    'dim_season_sql',
    'dim_date_sql',
]
