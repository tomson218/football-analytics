"""
main_dw_db.py — Orchestrator that creates the data warehouse schema
in the football_dw database.

Imports table definitions from `tables/` and executes them on the MySQL server.
"""
import mysql.connector
import os
import sys

# Add database/ directory to path to import the tables/ package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_config import get_db_host
from tables import TABLES

# Connect to MySQL server (without selecting a database, to create it first)
host_config = get_db_host()
cnx = mysql.connector.connect(**host_config)
cur = cnx.cursor()

# Create data warehouse database if it doesn't exist
db_name = "football_dw"
cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cur.execute(f"USE {db_name};")
print(f"Data warehouse database '{db_name}' is ready.")

# Execute table creation queries
for i, query in enumerate(TABLES, 1):
    try:
        cur.execute(query)
        print(f"[+] Table {i} created successfully.")
    except mysql.connector.Error as err:
        print(f"[-] Error creating table {i}: {err}")

# Commit changes and close connection
cnx.commit()
cur.close()
cnx.close()

print(f"\nData warehouse schema initialized: {len(TABLES)} tables in {db_name}!")
