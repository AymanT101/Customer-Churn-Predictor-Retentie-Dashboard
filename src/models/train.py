"""Train and evaluate the churn prediction model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from src.config import FEATURE_COLUMNS, METRICS_PATH, MODEL_DIR, MODEL_PATH, RAW_DATA_PATH, TARGET_COLUMN
from src.data.generate_data import main as generate_data
from src.models.preprocessing import build_preprocessor


def load_training_data(path: Path | None = None) -> pd.DataFrame:
    data_path = path or RAW_DATA_PATH
    if not data_path.exists():
        generate_data(output_path=data_path)
    return pd.read_csv(data_path)


def train_model(data_path: Path | None = None) -> dict:
    df = load_training_data(data_path)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor()
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train_prep, y_train)

    y_pred = model.predict(X_test_prep)
    y_proba = model.predict_proba(X_test_prep)[:, 1]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1": round(float(f1_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "churn_rate_pct": round(float(y.mean() * 100), 2),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {"preprocessor": preprocessor, "model": model}
    joblib.dump(artifact, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))

    print("Model saved to", MODEL_PATH)
    print(json.dumps(metrics, indent=2))
    print(classification_report(y_test, y_pred, target_names=["Retained", "Churned"]))
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train churn prediction model")
    parser.add_argument("--data", type=str, default=None, help="Path to training CSV")
    args = parser.parse_args()
    data_path = Path(args.data) if args.data else None
    train_model(data_path)


if __name__ == "__main__":
    main()
