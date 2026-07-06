"""Churn prediction inference helpers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.config import FEATURE_COLUMNS, MODEL_PATH, RISK_THRESHOLDS


def risk_label(probability: float) -> str:
    if probability >= RISK_THRESHOLDS["high"]:
        return "Critical"
    if probability >= RISK_THRESHOLDS["medium"]:
        return "High"
    if probability >= RISK_THRESHOLDS["low"]:
        return "Medium"
    return "Low"


def risk_factors(row: pd.Series) -> list[str]:
    """Human-readable retention signals for CS teams."""
    factors: list[str] = []

    if row["login_days_last_30"] < 8:
        factors.append("Lage productactiviteit (weinig logins)")
    if row["support_tickets_last_90"] >= 5:
        factors.append("Veel supporttickets — mogelijke frustratie")
    if row["feature_adoption_pct"] < 40:
        factors.append("Lage feature-adoptie — klant haalt weinig waarde uit product")
    if row["nps_score"] <= 6:
        factors.append("Lage NPS — ontevreden klant")
    if row["days_since_last_login"] > 14:
        factors.append("Lang niet ingelogd")
    if row["contract_months_remaining"] <= 2:
        factors.append("Contract loopt binnenkort af — renewal-moment")
    if row["onboarding_completed"] == "No":
        factors.append("Onboarding niet afgerond")
    if row["tenure_months"] < 6:
        factors.append("Jonge klant — hoger early-churn risico")

    return factors[:5] if factors else ["Geen kritieke signalen gedetecteerd"]


@lru_cache(maxsize=1)
def load_artifact(model_path: str | None = None):
    path = Path(model_path) if model_path else MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Model not found at {path}. Run: python -m src.models.train"
        )
    return joblib.load(path)


def predict_churn(
    customers: pd.DataFrame,
    model_path: str | None = None,
) -> pd.DataFrame:
    artifact = load_artifact(model_path)
    preprocessor = artifact["preprocessor"]
    model = artifact["model"]

    features = customers[FEATURE_COLUMNS]
    X = preprocessor.transform(features)
    probabilities = model.predict_proba(X)[:, 1]

    result = customers.copy()
    result["churn_probability"] = np.round(probabilities, 4)
    result["churn_prediction"] = (probabilities >= 0.5).astype(int)
    result["risk_level"] = [risk_label(p) for p in probabilities]
    result["risk_factors"] = customers.apply(risk_factors, axis=1)
    return result
