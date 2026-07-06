"""Shared configuration and feature definitions."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "customers.csv"
MODEL_DIR = PROJECT_ROOT / "models" / "artifacts"
MODEL_PATH = MODEL_DIR / "churn_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

NUMERIC_FEATURES = [
    "tenure_months",
    "mrr_eur",
    "seats",
    "login_days_last_30",
    "support_tickets_last_90",
    "feature_adoption_pct",
    "nps_score",
    "days_since_last_login",
    "contract_months_remaining",
]

CATEGORICAL_FEATURES = [
    "plan_tier",
    "industry",
    "payment_method",
    "onboarding_completed",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "churned"

RISK_THRESHOLDS = {
    "low": 0.25,
    "medium": 0.55,
    "high": 0.75,
}

API_HOST = "0.0.0.0"
API_PORT = 8000
DASHBOARD_PORT = 8501
