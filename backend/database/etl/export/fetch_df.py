"""
fetch_df.py — Run a query and return the result as a DataFrame.
"""
import pandas as pd


def fetch_df(cursor, query):
    """Execute `query` and return all rows as a DataFrame."""
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
