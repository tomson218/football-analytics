"""
plot_training_curves.py — Plot CatBoost training curves from catboost_info/ logs.

CatBoost writes a training log to catboost_info/ in the directory the training
was started from, and each run overwrites the previous one. The committed logs are:
  - backend/catboost_info/                         -> 6-feature model (100 iterations)
  - backend/ml_exploratory_analysis/catboost_info/ -> base model (300 iterations)
(Their last validation row matches the model's validation metrics in
results/model_comparison.json.)

For each model, two panels:
  - Log loss per iteration, train vs validation (a widening gap means overfitting).
  - Validation AUC per iteration (CatBoost does not compute AUC on the train set).

Export: docs/images/training_curves.png

Run from the backend/ directory:
    python ml_exploratory_analysis/plot_training_curves.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BACKEND = Path(__file__).resolve().parents[1]
OUTPUT = BACKEND.parent / "docs" / "images" / "training_curves.png"

MODELS = [
    ("6-feature model (used by the API)", BACKEND / "catboost_info"),
    ("Base model (25 features)", BACKEND / "ml_exploratory_analysis" / "catboost_info"),
]

# Colors and chart chrome (validated categorical slots 1-2 on a light surface)
TRAIN, VALIDATION = "#2a78d6", "#eb6834"
SURFACE, INK, INK_2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"


def style(ax, title, ylabel):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=10)
    ax.set_xlabel("Iteration", fontsize=9, color=MUTED)
    ax.set_ylabel(ylabel, fontsize=9, color=MUTED)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8, length=0)


def end_label(ax, df, column, color, text, dy=0):
    """Label a line at its last point with the series name and final value.
    dy shifts the label vertically (points) so close labels don't overlap."""
    x, y = df["iter"].iloc[-1], df[column].iloc[-1]
    ax.plot(x, y, "o", color=color, markersize=5, markeredgecolor=SURFACE, markeredgewidth=1.5)
    ax.annotate(f"{text} {y:.3f}", (x, y), xytext=(6, dy), textcoords="offset points",
                va="center", fontsize=8, color=INK_2)


def main():
    fig, axes = plt.subplots(len(MODELS), 2, figsize=(12, 4.2 * len(MODELS)), facecolor=SURFACE)

    for row, (name, folder) in enumerate(MODELS):
        learn = pd.read_csv(folder / "learn_error.tsv", sep="\t")
        test = pd.read_csv(folder / "test_error.tsv", sep="\t")
        loss_ax, auc_ax = axes[row]

        # Log loss: train vs validation
        loss_ax.plot(learn["iter"], learn["Logloss"], color=TRAIN, linewidth=2, label="Train")
        loss_ax.plot(test["iter"], test["Logloss"], color=VALIDATION, linewidth=2, label="Validation")
        # Spread the two end labels apart when the final values are close
        train_end, val_end = learn["Logloss"].iloc[-1], test["Logloss"].iloc[-1]
        spread = 6 if abs(train_end - val_end) < 0.01 else 0
        train_up = train_end > val_end
        end_label(loss_ax, learn, "Logloss", TRAIN, "Train", spread if train_up else -spread)
        end_label(loss_ax, test, "Logloss", VALIDATION, "Validation", -spread if train_up else spread)
        style(loss_ax, f"{name}: log loss (lower is better)", "Log loss")
        loss_ax.legend(frameon=False, fontsize=8, labelcolor=INK_2, loc="upper right")

        # AUC: validation only
        auc_ax.plot(test["iter"], test["AUC"], color=VALIDATION, linewidth=2)
        best = test.loc[test["AUC"].idxmax()]
        auc_ax.plot(best["iter"], best["AUC"], "o", color=VALIDATION, markersize=5,
                    markeredgecolor=SURFACE, markeredgewidth=1.5)
        auc_ax.annotate(f"best {best['AUC']:.3f} (iter {int(best['iter'])})", (best["iter"], best["AUC"]),
                        xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8, color=INK_2)
        end_label(auc_ax, test, "AUC", VALIDATION, "final")
        style(auc_ax, f"{name}: validation AUC (higher is better)", "AUC")

        for ax in (loss_ax, auc_ax):
            ax.set_xlim(0, test["iter"].iloc[-1] * 1.18)  # room for end labels

    fig.tight_layout(h_pad=3)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=110, facecolor=SURFACE)
    print(f"Training curves saved -> {OUTPUT}")


if __name__ == "__main__":
    main()
