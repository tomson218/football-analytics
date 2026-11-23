"""
train_models.py — Train 3 CatBoost models from scratch on raw data (no scaler).

1. **Base Model** — 25 features (all numerical features from matches_cleaned.csv)
2. **10-Feature Model** — 10 top features selected by importance from the base model.
3. **6-Feature Model** — 6 top features selected by importance from the base model.

Each model is trained with grid search + 5-fold CV.

CatBoost works with raw data — no feature scaling is needed.

Output:
  - models/catboost_base.cbm
  - models/catboost_10feat.cbm
  - models/catboost_6feat.cbm
  - results/model_comparison.json
  - results/model_comparison_table.csv
  - results/feature_importance_base.png
  - results/feature_importance_10feat.png
  - results/feature_importance_6feat.png
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from catboost import CatBoostClassifier, Pool
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, log_loss
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import json
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from common.constants import FEATURE_COLS_BASE, FEATURE_COLS_10, FEATURE_COLS_6

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
models_dir = os.path.join(script_dir, "models")
results_dir = os.path.join(script_dir, "results")
os.makedirs(models_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Load data — raw, no scaling
# ---------------------------------------------------------------------------
df = pd.read_csv(os.path.join(data_dir, "matches_cleaned.csv"))
y_binary = pd.read_csv(os.path.join(data_dir, "y_binary.csv"))["HomeNoLose"].values

print(f"Loaded data: {df.shape[0]} matches")

# Split: 80% train+val, 10% test (stratified)
X = df[FEATURE_COLS_BASE].values
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y_binary, test_size=0.1, stratify=y_binary, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=1/9, stratify=y_temp, random_state=42
)

print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

# ---------------------------------------------------------------------------
# Helper: train a model with grid search
# ---------------------------------------------------------------------------
def train_model(feature_names, model_name, model_filename):
    """Train a CatBoost model with grid search and return metrics + model."""
    feat_indices = [FEATURE_COLS_BASE.index(f) for f in feature_names]

    print(f"\n{'='*60}")
    print(f"Training: {model_name} ({len(feature_names)} features)")
    print(f"{'='*60}")
    print(f"Features: {feature_names}")

    # Select features by index
    X_tr = X_train[:, feat_indices]
    X_va = X_val[:, feat_indices]
    X_te = X_test[:, feat_indices]

    train_pool = Pool(X_tr, y_train)
    val_pool = Pool(X_va, y_val)

    # Grid search
    param_grid = {
        'iterations': [100, 300, 500],
        'depth': [4, 5, 6],
        'learning_rate': [0.03, 0.05, 0.1],
        'l2_leaf_reg': [1, 3, 5],
        'border_count': [64, 128],
    }

    model = CatBoostClassifier(
        loss_function='Logloss',
        eval_metric='AUC',
        random_seed=42,
        thread_count=-1,
        verbose=False,
        early_stopping_rounds=100
    )

    print("  Grid search with 5-fold CV...")
    grid_result = model.grid_search(param_grid, train_pool, cv=5, plot=False, verbose=0)

    best_params = grid_result["params"]
    cv_auc_mean = max(grid_result["cv_results"]["test-AUC-mean"])
    cv_auc_std = grid_result["cv_results"]["test-AUC-std"][
        np.argmax(grid_result["cv_results"]["test-AUC-mean"])
    ]
    print(f"  CV AUC: {cv_auc_mean:.4f} +/- {cv_auc_std:.4f}")
    print(f"  Best params: {best_params}")

    # Train final model
    final_model = CatBoostClassifier(
        **best_params,
        loss_function='Logloss',
        custom_metric=['AUC', 'Accuracy', 'Precision', 'Recall'],
        eval_metric='AUC',
        random_seed=42,
        thread_count=-1,
        verbose=False
    )

    start_time = time.time()
    final_model.fit(train_pool, eval_set=val_pool, plot=False)
    training_time = time.time() - start_time

    # Validation metrics
    history = final_model.get_evals_result()
    val_auc = history['validation']['AUC'][-1]
    val_accuracy = history['validation']['Accuracy'][-1]
    val_precision = history['validation']['Precision'][-1]
    val_recall = history['validation']['Recall'][-1]
    val_logloss = history['validation']['Logloss'][-1]

    # Test metrics
    y_pred_proba = final_model.predict_proba(X_te)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)

    test_acc = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred)
    test_auc = roc_auc_score(y_test, y_pred_proba)
    test_logloss = log_loss(y_test, y_pred_proba)

    # Feature importance
    fi = final_model.get_feature_importance(type='PredictionValuesChange')
    fi_dict = {name: float(imp) for name, imp in zip(feature_names, fi)}

    # Save model
    model_path = os.path.join(models_dir, model_filename)
    final_model.save_model(model_path)
    print(f"  Model saved -> {model_path}")

    print(f"\n  {'-'*40}")
    print(f"  Validation Metrics:")
    print(f"    AUC       : {val_auc:.4f}")
    print(f"    Accuracy  : {val_accuracy:.4f}")
    print(f"    Precision : {val_precision:.4f}")
    print(f"    Recall    : {val_recall:.4f}")
    print(f"    LogLoss   : {val_logloss:.4f}")
    print(f"  {'-'*40}")
    print(f"  Test Metrics:")
    print(f"    AUC       : {test_auc:.4f}")
    print(f"    Accuracy  : {test_acc:.4f}")
    print(f"    F1        : {test_f1:.4f}")
    print(f"    LogLoss   : {test_logloss:.4f}")
    print(f"  {'-'*40}")
    print(f"  Feature Importance (sorted descending):")
    sorted_fi = sorted(fi_dict.items(), key=lambda x: x[1], reverse=True)
    cumsum = 0.0
    for feat, imp in sorted_fi:
        cumsum += imp
        print(f"    {feat}: {imp:.2f}% (cumulative: {cumsum:.2f}%)")

    return {
        "model_name": model_name,
        "features_count": len(feature_names),
        "features": feature_names,
        "best_params": {k: (int(v) if isinstance(v, (np.integer,)) else float(v) if isinstance(v, (np.floating,)) else v) for k, v in best_params.items()},
        "cv_auc_mean": float(cv_auc_mean),
        "cv_auc_std": float(cv_auc_std),
        "training_time_sec": float(training_time),
        "validation_metrics": {
            "AUC": float(val_auc),
            "Accuracy": float(val_accuracy),
            "Precision": float(val_precision),
            "Recall": float(val_recall),
            "Logloss": float(val_logloss)
        },
        "test_metrics": {
            "AUC": float(test_auc),
            "Accuracy": float(test_acc),
            "F1": float(test_f1),
            "Logloss": float(test_logloss)
        },
        "feature_importance": fi_dict
    }

# ---------------------------------------------------------------------------
# 1. Base Model — 25 features (all)
# ---------------------------------------------------------------------------
base_result = train_model(
    list(FEATURE_COLS_BASE),
    "Base (25 features)",
    "catboost_base.cbm"
)

# ---------------------------------------------------------------------------
# 2. 10-Feature Model — top features by importance
# ---------------------------------------------------------------------------
ten_result = train_model(
    list(FEATURE_COLS_10),
    "10-Feature (top 10)",
    "catboost_10feat.cbm"
)

# ---------------------------------------------------------------------------
# 3. 6-Feature Model — top 6 features by importance
# ---------------------------------------------------------------------------
six_result = train_model(
    list(FEATURE_COLS_6),
    "6-Feature (top 6)",
    "catboost_6feat.cbm"
)

# ---------------------------------------------------------------------------
# Comparison table
# ---------------------------------------------------------------------------
print(f"\n\n{'='*80}")
print("MODEL COMPARISON TABLE")
print(f"{'='*80}")

comparison = [base_result, ten_result, six_result]

rows = []
for res in comparison:
    row = {
        "Model": res["model_name"],
        "Features": res["features_count"],
        "Feature List": ", ".join(res["features"]),
        "CV AUC": f"{res['cv_auc_mean']:.4f}",
        "CV AUC Std": f"{res['cv_auc_std']:.4f}",
        "Val AUC": f"{res['validation_metrics']['AUC']:.4f}",
        "Val Accuracy": f"{res['validation_metrics']['Accuracy']:.4f}",
        "Val Precision": f"{res['validation_metrics']['Precision']:.4f}",
        "Val Recall": f"{res['validation_metrics']['Recall']:.4f}",
        "Val LogLoss": f"{res['validation_metrics']['Logloss']:.4f}",
        "Test AUC": f"{res['test_metrics']['AUC']:.4f}",
        "Test Accuracy": f"{res['test_metrics']['Accuracy']:.4f}",
        "Test F1": f"{res['test_metrics']['F1']:.4f}",
        "Test LogLoss": f"{res['test_metrics']['Logloss']:.4f}",
        "Training Time (s)": f"{res['training_time_sec']:.2f}",
    }
    rows.append(row)

comparison_df = pd.DataFrame(rows)
print(comparison_df.to_string(index=False))

csv_path = os.path.join(results_dir, "model_comparison_table.csv")
comparison_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"\nComparison table saved -> {csv_path}")

# ---------------------------------------------------------------------------
# Save full results to JSON
# ---------------------------------------------------------------------------
full_results = {
    "comparison": comparison,
    "summary": {
        "base_model": {
            "features_count": base_result["features_count"],
            "test_auc": base_result["test_metrics"]["AUC"],
            "test_accuracy": base_result["test_metrics"]["Accuracy"],
            "test_f1": base_result["test_metrics"]["F1"]
        },
        "ten_feature_model": {
            "features_count": ten_result["features_count"],
            "features": ten_result["features"],
            "test_auc": ten_result["test_metrics"]["AUC"],
            "test_accuracy": ten_result["test_metrics"]["Accuracy"],
            "test_f1": ten_result["test_metrics"]["F1"]
        },
        "six_feature_model": {
            "features_count": six_result["features_count"],
            "features": six_result["features"],
            "test_auc": six_result["test_metrics"]["AUC"],
            "test_accuracy": six_result["test_metrics"]["Accuracy"],
            "test_f1": six_result["test_metrics"]["F1"]
        }
    }
}

json_path = os.path.join(results_dir, "model_comparison.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(full_results, f, indent=2, ensure_ascii=False)
print(f"\nFull results saved -> {json_path}")

# ---------------------------------------------------------------------------
# Visualization: Feature importance bar charts (one per model)
# ---------------------------------------------------------------------------
for res in comparison:
    fi_sorted = sorted(res["feature_importance"].items(), key=lambda x: x[1], reverse=True)
    feats, imps = zip(*fi_sorted)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(feats)))

    fig, ax = plt.subplots(figsize=(10, max(4, len(feats) * 0.5)))
    ax.barh(range(len(feats)), imps, color=colors)
    ax.set_yticks(range(len(feats)))
    ax.set_yticklabels(feats, fontsize=10)
    ax.set_xlabel("Importance (%)")
    ax.set_title(f"{res['model_name']}\nTest AUC: {res['test_metrics']['AUC']:.4f}")
    ax.invert_yaxis()

    plt.tight_layout()
    # Determine filename
    if "Base" in res["model_name"]:
        plot_path = os.path.join(results_dir, "feature_importance_base.png")
    elif "10-Feature" in res["model_name"]:
        plot_path = os.path.join(results_dir, "feature_importance_10feat.png")
    elif "6-Feature" in res["model_name"]:
        plot_path = os.path.join(results_dir, "feature_importance_6feat.png")
    else:
        plot_path = os.path.join(results_dir, f"feature_importance_{res['model_name'].replace(' ', '_').lower()}.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Feature importance chart saved -> {plot_path}")

# ---------------------------------------------------------------------------
# Print summary for README
# ---------------------------------------------------------------------------
print(f"\n\n{'='*60}")
print("TRAINING COMPLETE — Summary for README.md")
print(f"{'='*60}")
for res in comparison:
    print(f"\n{res['model_name']}:")
    print(f"  Test AUC:      {res['test_metrics']['AUC']:.4f}")
    print(f"  Test Accuracy: {res['test_metrics']['Accuracy']:.4f}")
    print(f"  Test F1:       {res['test_metrics']['F1']:.4f}")
    print(f"  Test LogLoss:  {res['test_metrics']['Logloss']:.4f}")
    print(f"  CV AUC:        {res['cv_auc_mean']:.4f} +/- {res['cv_auc_std']:.4f}")
    print(f"  Training Time: {res['training_time_sec']:.2f}s")
    print(f"  Best params:   {res['best_params']}")
    print(f"  Feature Importance (sorted descending):")
    for feat, imp in sorted(res["feature_importance"].items(), key=lambda x: x[1], reverse=True):
        print(f"    {feat}: {imp:.2f}%")

print(f"\n{'='*60}")
