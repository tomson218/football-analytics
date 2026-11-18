#!/bin/bash

echo "========================================"
echo " ETL Pipeline — Raw CSV to Data Warehouse"
echo "========================================"
echo

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH!"
    exit 1
fi

echo "[+] Python found."
echo

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "[+] Activating virtual environment..."
    source venv/bin/activate
else
    echo "[-] No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "[+] Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo
echo "========================================"
echo " Step 1: Creating database schema..."
echo "========================================"
python database/main_dw_db.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Schema creation failed!"
    exit 1
fi

echo
echo "========================================"
echo " Step 2: Running ETL (CSV to Data Warehouse)..."
echo "========================================"
python database/etl/etl_raw_to_dw.py
if [ $? -ne 0 ]; then
    echo "[ERROR] ETL failed!"
    exit 1
fi

echo
echo "========================================"
echo " ETL Pipeline Completed Successfully!"
echo "========================================"
echo
echo "Data warehouse (football_dw) is ready with:"
echo "  - 5 dimension tables (dim_country, dim_division, dim_team, dim_season, dim_date)"
echo "  - 1 fact table (fact_matches)"
echo "  - 2 raw staging tables (raw_eloRatings, raw_Matches)"
echo "  - CSV exports in csv/raw/ and csv/clean/"
echo
