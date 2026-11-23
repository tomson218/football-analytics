#!/bin/bash

echo "========================================"
echo " ML Pipeline — HomeNoLose Classification"
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
echo " Step 1: Preparing Data from Data Warehouse..."
echo "========================================"
python ml_exploratory_analysis/prepare_data.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Data preparation failed!"
    exit 1
fi

echo
echo "========================================"
echo " Step 2: Processing Features (Scaling + Target)..."
echo "========================================"
python ml_exploratory_analysis/data_processing.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Data processing failed!"
    exit 1
fi

echo
echo "========================================"
echo " Step 3: Training CatBoost Model (5-fold CV)..."
echo "========================================"
python ml_exploratory_analysis/train_models.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Model training failed!"
    exit 1
fi

echo
echo "========================================"
echo " Step 4: Testing Model on Test Set..."
echo "========================================"
python ml_exploratory_analysis/testing.py
if [ $? -ne 0 ]; then
    echo "[ERROR] Model testing failed!"
    exit 1
fi

echo
echo "========================================"
echo " ML Pipeline Completed Successfully!"
echo "========================================"
echo
echo "Results:"
echo "  - Models saved: ml_exploratory_analysis/models/catboost_base.cbm, catboost_10feat.cbm, catboost_6feat.cbm"
echo "  - Metrics: ml_exploratory_analysis/results/model_comparison.json, binary_results.json"
echo "  - Confusion matrix: ml_exploratory_analysis/results/confusion_matrix.png"
echo "  - Feature importance: ml_exploratory_analysis/results/feature_importance_base.png, feature_importance_10feat.png, feature_importance_6feat.png"
echo "  - Sample predictions: ml_exploratory_analysis/results/sample_matches_test.csv"
echo
