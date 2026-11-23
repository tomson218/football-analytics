"""
testing.py — Evaluate CatBoost model on test set.
Load model + test data, calculate metrics (Accuracy, F1, ROC AUC, LogLoss),
confusion matrix (seaborn heatmap) and 20 sample matches with predictions.

Uses the base model (25 features).

Export:
  - results/sample_matches_test.csv — 20 matches with predictions
  - results/confusion_matrix.png — confusion matrix
  - results/binary_results.json — full results (test + CV + validation)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, roc_auc_score, log_loss
from catboost import CatBoostClassifier
from common.constants import FEATURE_COLS_BASE
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # No GUI — save to file
import matplotlib.pyplot as plt
import json

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
models_dir = os.path.join(script_dir, "models")
results_dir = os.path.join(script_dir, "results")
os.makedirs(results_dir, exist_ok=True)

# Load model (base model — 25 features)
final_model = CatBoostClassifier()
model_path = os.path.join(models_dir, "catboost_base.cbm")
final_model.load_model(model_path)
print(f"Model loaded from {model_path}")

# Load test data
matches = pd.read_csv(os.path.join(data_dir, "matches_cleaned.csv"))
y_binary = pd.read_csv(os.path.join(data_dir, "y_binary.csv"))["HomeNoLose"].values

# Use the same train/test split as train_models.py
from sklearn.model_selection import train_test_split
X = matches[FEATURE_COLS_BASE].values
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y_binary, test_size=0.1, stratify=y_binary, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=1/9, stratify=y_temp, random_state=42
)

# Load training results
with open(os.path.join(results_dir, "model_comparison.json"), "r") as f:
    model_results = json.load(f)

result = model_results["comparison"][0]  # Base model (25 features)

cv_auc_mean = result["cv_auc_mean"]
training_time = result["training_time_sec"]
best_params = result["best_params"]
cv_auc_std = result["cv_auc_std"]

val_auc = result["validation_metrics"]["AUC"]
val_accuracy = result["validation_metrics"]["Accuracy"]
val_precision = result["validation_metrics"]["Precision"]
val_recall = result["validation_metrics"]["Recall"]
val_logloss = result["validation_metrics"]["Logloss"]

print(f"Best parameters: {best_params}")

# Predictions on test set
y_pred_proba = final_model.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba >= 0.5).astype(int)

# Test metrics
acc  = accuracy_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)
auc  = roc_auc_score(y_test, y_pred_proba)
logloss_val = log_loss(y_test, y_pred_proba)

print(f"\n{'='*40}")
print(f"TESTING RESULTS")
print(f"{'='*40}")
print(f"Accuracy : {acc:.4f}")
print(f"F1-score : {f1:.4f}")
print(f"ROC AUC  : {auc:.4f}")
print(f"LogLoss   : {logloss_val:.4f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(7, 6))
sns.heatmap(
    cm, annot=True, fmt='d', cmap='Blues',
    xticklabels=['Away Win (A)', 'Home No Lose (H/D)'],
    yticklabels=['Away Win (A)', 'Home No Lose (H/D)']
)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title(f'Confusion Matrix – Test AUC: {auc:.4f}')
plt.tight_layout()
cm_path = os.path.join(results_dir, "confusion_matrix.png")
plt.savefig(cm_path, dpi=150)
plt.close()
print(f"\nConfusion matrix saved -> {cm_path}")

# Full results in JSON
results = {
    "task": "HomeNoLose vs AwayWin",
    "model": "Base (25 features)",
    "cv_auc_mean": float(cv_auc_mean),
    "cv_auc_std": float(cv_auc_std),
    "test_accuracy": float(acc),
    "test_f1": float(f1),
    "test_auc": float(auc),
    "test_logloss": float(logloss_val),
    "training_time_sec": float(training_time),
    "best_params": best_params,
    "final_validation_metrics": {
        "AUC": float(val_auc),
        "Accuracy": float(val_accuracy),
        "Precision": float(val_precision),
        "Recall": float(val_recall),
        "Logloss": float(val_logloss)
    }
}

with open(os.path.join(results_dir, "binary_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Results updated -> results/binary_results.json")

# 20 sample matches from test data
print(f"\n\n{'='*40}")
print("20 SAMPLE MATCHES FROM TEST DATA")
print(f"{'='*40}")

np.random.seed(42)
idx = np.random.choice(len(X_test), size=20, replace=False)

# Build display DataFrame from matches_cleaned.csv
display_data = {}
for i, feat in enumerate(FEATURE_COLS_BASE):
    display_data[feat] = X_test[idx, i]

display_df = pd.DataFrame(display_data)
display_df['P(HomeNoLose)'] = y_pred_proba[idx].round(4)
display_df['Predicted'] = ['HomeNoLose' if p >= 0.5 else 'AwayWin' for p in y_pred_proba[idx]]
display_df['Actual'] = ['HomeNoLose' if real == 1 else 'AwayWin' for real in y_test[idx]]
display_df['VERDICT'] = [
    'CORRECT' if pred == actual else 'ERROR'
    for pred, actual in zip(display_df['Predicted'], display_df['Actual'])
]

display_df = display_df.reset_index(drop=True)
display_df.index += 1
display_df = display_df.rename_axis('No.')

print(display_df.to_string(float_format="{:.2f}".format))

# Save sample matches
csv_path = os.path.join(results_dir, "sample_matches_test.csv")
display_df.to_csv(csv_path, index=True, encoding='utf-8-sig')
print(f"\nSample matches saved -> {csv_path}")

print(f"\n{'='*40}")
print("TESTING COMPLETE")
print(f"{'='*40}")
print(f"Test Accuracy: {acc:.4f}")
print(f"Test F1: {f1:.4f}")
print(f"Test AUC: {auc:.4f}")
print(f"Test LogLoss: {logloss_val:.4f}")
