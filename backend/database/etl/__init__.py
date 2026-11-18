"""
etl/__init__.py — ETL module for football_dw data warehouse.

Contains subfolders (one file per function):
- extract/ — Extract raw data from CSV to raw_* tables.
- clean/ — Clean data (Elo, form, odds, statistics).
- dimensions/ — Load 5 dimension tables.
- facts/ — Load fact table (fact_matches).
- export/ — Export raw data and dimension tables to CSV.
- etl_raw_to_dw.py — Main ETL orchestrator.

Run:
    python backend/database/etl/etl_raw_to_dw.py
"""
