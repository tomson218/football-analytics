"""
read_sql.py — Execute a SQL query and return a DataFrame.
"""
import mysql.connector
import pandas as pd

from database.db_config import get_db_config


def read_sql_to_df(query: str) -> pd.DataFrame:
    """
    Execute a SQL query against the data warehouse and return a DataFrame.
    The connection is automatically closed after the query.
    """
    dw_config = get_db_config()
    cnx = mysql.connector.connect(**dw_config)
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df
