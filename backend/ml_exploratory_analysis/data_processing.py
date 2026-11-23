"""
data_processing.py — Create HomeNoLose target variable from cleaned match data.
Reads data/matches_cleaned.csv and creates the binary target variable:
HomeNoLose = (FTResult == 'H') | (FTResult == 'D') → 1 or 0.

CatBoost does not require feature scaling, so no scaler is used.
The training script reads matches_cleaned.csv directly.

Export: data/y_binary.csv
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import pandas as pd
from common.constants import FEATURE_COLS_BASE

# Path to data/ folder
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")

# Load cleaned data
df = pd.read_csv(os.path.join(data_dir, "matches_cleaned.csv"))
print(f"Loaded {len(df)} matches from matches_cleaned.csv")

# Verify all feature columns exist
missing = set(FEATURE_COLS_BASE) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in matches_cleaned.csv: {missing}")

y = df['FTResult'].copy()

# Target variable: HomeNoLose (home team did not lose: H or D = 1, A = 0)
y_binary = pd.DataFrame({
    "HomeNoLose": ((y == 'H') | (y == 'D')).astype(int),
    "AwayWin":    (y == 'A').astype(int)
}, index=df.index)

# Save results
os.makedirs(data_dir, exist_ok=True)

y_binary.to_csv(os.path.join(data_dir, "y_binary.csv"), index=False)

print("\nClass distribution:")
print(y_binary.mean())
print(f"\nHomeNoLose (1): {(y_binary['HomeNoLose'] == 1).sum()} matches")
print(f"AwayWin (0):    {(y_binary['HomeNoLose'] == 0).sum()} matches")
print(f"\nData saved:")
print(f"  -> {os.path.join(data_dir, 'y_binary.csv')}")
print(f"  (No scaler needed — CatBoost works with raw data)")
