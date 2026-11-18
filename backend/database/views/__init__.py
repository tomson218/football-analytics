"""
views/__init__.py — Collects all SQL view definitions for the data warehouse.

Each view in a separate file. Views are created after tables,
so they must be executed after TABLES.
"""

from views.v_matches_enriched import SQL as v_matches_enriched_sql

VIEWS = [
    v_matches_enriched_sql,
]
