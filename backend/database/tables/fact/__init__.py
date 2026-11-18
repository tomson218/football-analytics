"""
tables/fact/__init__.py — Re-exports fact table definitions.
"""
from .fact_matches import SQL as fact_matches_sql

__all__ = [
    'fact_matches_sql',
]
