#!/bin/bash

echo "========================================"
echo " Statistical Analysis — Stats + Charts"
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
echo " Step 1: Running Descriptive Statistics..."
echo "========================================"
python -m statistical_analysis.run_stats
if [ $? -ne 0 ]; then
    echo "[ERROR] Descriptive statistics failed!"
    exit 1
fi

echo
echo "========================================"
echo " Step 2: Generating Charts..."
echo "========================================"
python -m statistical_analysis.visualisation_data
if [ $? -ne 0 ]; then
    echo "[ERROR] Chart generation failed!"
    exit 1
fi

echo
echo "========================================"
echo " Statistical Analysis Completed!"
echo "========================================"
echo
echo "Results:"
echo "  - Descriptive stats printed to console"
echo "  - Correlation matrix saved to correlation_matrix.xlsx"
echo "  - 9 charts displayed one after another"
echo
