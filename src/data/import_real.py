"""Import real-world churn datasets into the project schema."""

from __future__ import annotations

import argparse
import io
from pathlib import Path
from urllib.request import urlopen

import numpy as np
import pandas as pd

from src.config import (
    CATEGORICAL_FEATURES,
    FEATURE_COLUMNS,
    NUMERIC_FEATURES,
    RAW_DATA_PATH,
    TARGET_COLUMN,
)
from src.data.generate_data import INDUSTRIES, PLAN_TIERS

TELCO_URLS = [
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv",
    "https://community.ibm.com/HigherLogic/System/DownloadDocumentFile.ashx?DocumentFileKey=205ACA47-22E9-5FEE-9DA1-BDE76D254C31&forceDialog=0",
]

REQUIRED_COLUMNS = FEATURE_COLUMNS + ["customer_id", "company_name", TARGET_COLUMN]

PAYMENT_MAP = {
    "Electronic check": "Credit Card",
    "Mailed check": "Invoice",
    "Bank transfer (automatic)": "SEPA",
    "Credit card (automatic)": "Credit Card",
}

CONTRACT_TO_PLAN = {
    "Month-to-month": "Starter",
    "One year": "Professional",
    "Two year": "Enterprise",
}


def _validate_schema(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV mist verplichte kolommen: {', '.join(missing)}")

    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"Kolom '{col}' bevat niet-numerieke waarden")

    for col in CATEGORICAL_FEATURES:
        if df[col].isna().any():
            raise ValueError(f"Kolom '{col}' bevat lege waarden")

    if not df["churned"].isin([0, 1]).all():
        raise ValueError("Kolom 'churned' moet 0 of 1 bevatten")

    valid_plans = set(PLAN_TIERS)
    if not set(df["plan_tier"].unique()).issubset(valid_plans):
        invalid = set(df["plan_tier"].unique()) - valid_plans
        raise ValueError(f"Ongeldige plan_tier waarden: {invalid}")

    valid_industries = set(INDUSTRIES)
    if not set(df["industry"].unique()).issubset(valid_industries):
        invalid = set(df["industry"].unique()) - valid_industries
        raise ValueError(f"Ongeldige industry waarden: {invalid}")


def _service_yes_count(row: pd.Series, columns: list[str]) -> int:
    return sum(1 for col in columns if str(row.get(col, "")).strip().lower() in {"yes", "1", "true"})


def map_telco_to_schema(raw: pd.DataFrame) -> pd.DataFrame:
    """Map IBM Telco Customer Churn CSV to B2B SaaS feature schema."""
    df = raw.copy()
    df.columns = [c.strip() for c in df.columns]

    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

    service_cols = [
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]
    available_services = [c for c in service_cols if c in df.columns]

    rng = np.random.default_rng(42)
    n = len(df)

    adoption_pct = df.apply(lambda row: _service_yes_count(row, available_services), axis=1)
    max_services = max(len(available_services), 1)
    feature_adoption = (adoption_pct / max_services * 100).clip(5, 100)

    if "TechSupport" in df.columns:
        tech_support_no = df["TechSupport"].astype(str).str.lower().eq("no").to_numpy()
    else:
        tech_support_no = np.zeros(n, dtype=bool)

    if "InternetService" in df.columns:
        internet_fiber = df["InternetService"].astype(str).str.lower().eq("fiber optic").to_numpy()
    else:
        internet_fiber = np.zeros(n, dtype=bool)

    login_days = np.where(internet_fiber, rng.integers(0, 14, size=n), rng.integers(4, 28, size=n))
    login_days = np.where(tech_support_no, login_days - 3, login_days)
    login_days = np.clip(login_days, 0, 30)

    support_tickets = np.where(tech_support_no, rng.integers(4, 12, size=n), rng.poisson(2, size=n))

    nps = np.clip(10 - support_tickets // 2 + (feature_adoption.to_numpy() / 20).astype(int), 0, 10)

    days_since_login = np.clip(30 - login_days + rng.integers(0, 8, size=n), 0, 45)

    contract = df["Contract"]
    contract_remaining = np.ones(n, dtype=int)
    one_year = contract == "One year"
    two_year = contract == "Two year"
    contract_remaining[one_year.to_numpy()] = rng.integers(3, 12, size=int(one_year.sum()))
    contract_remaining[two_year.to_numpy()] = rng.integers(6, 24, size=int(two_year.sum()))

    if "OnlineSecurity" in df.columns:
        onboarding = np.where(
            (df["OnlineSecurity"].astype(str).str.lower() == "yes") & (feature_adoption > 40),
            "Yes",
            "No",
        )
    else:
        onboarding = np.where(feature_adoption > 50, "Yes", "No")

    industry_idx = rng.integers(0, len(INDUSTRIES), size=n)

    mapped = pd.DataFrame(
        {
            "customer_id": df["customerID"].astype(str),
            "company_name": "Klant " + df["customerID"].astype(str).str[-4:],
            "tenure_months": df["tenure"].astype(int).clip(1, 72),
            "mrr_eur": pd.to_numeric(df["MonthlyCharges"], errors="coerce").round(2).clip(49, 8000),
            "seats": np.clip((df["MonthlyCharges"] / 25).astype(int), 1, 120),
            "plan_tier": df["Contract"].map(CONTRACT_TO_PLAN).fillna("Professional"),
            "industry": [INDUSTRIES[i] for i in industry_idx],
            "payment_method": df["PaymentMethod"].map(PAYMENT_MAP).fillna("Credit Card"),
            "onboarding_completed": onboarding,
            "login_days_last_30": login_days.astype(int),
            "support_tickets_last_90": support_tickets.astype(int),
            "feature_adoption_pct": feature_adoption.round(1),
            "nps_score": nps.astype(int),
            "days_since_last_login": days_since_login.astype(int),
            "contract_months_remaining": contract_remaining,
            "churned": (df["Churn"].astype(str).str.lower() == "yes").astype(int),
        }
    )
    return mapped


def download_telco() -> pd.DataFrame:
    """Download IBM Telco Customer Churn dataset."""
    last_error: Exception | None = None
    for url in TELCO_URLS:
        try:
            with urlopen(url, timeout=30) as response:
                content = response.read().decode("utf-8")
            return pd.read_csv(io.StringIO(content))
        except Exception as exc:  # noqa: BLE001 — try next mirror
            last_error = exc
    raise RuntimeError("Kon Telco-dataset niet downloaden. Probeer --source file.") from last_error


def import_telco(output_path: Path | None = None) -> Path:
    """Download Telco data, map to schema, and save CSV."""
    raw = download_telco()
    mapped = map_telco_to_schema(raw)
    _validate_schema(mapped)
    return save_customers(mapped, output_path)


def import_custom_csv(source_path: Path, output_path: Path | None = None) -> Path:
    """Import a CSV that already matches the project schema."""
    df = pd.read_csv(source_path)
    _validate_schema(df)
    return save_customers(df, output_path)


def save_customers(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    path = output_path or RAW_DATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df[REQUIRED_COLUMNS].to_csv(path, index=False)
    churn_rate = df[TARGET_COLUMN].mean() * 100
    print(f"Imported {len(df)} customers -> {path}")
    print(f"Churn rate: {churn_rate:.1f}%")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Import real churn dataset")
    parser.add_argument(
        "--source",
        choices=["telco", "file"],
        default="telco",
        help="Dataset source: telco (IBM public data) or file (your own CSV)",
    )
    parser.add_argument("--input", type=str, default=None, help="Path to your CSV when --source file")
    parser.add_argument("--output", type=str, default=None, help="Output path (default: data/raw/customers.csv)")
    args = parser.parse_args()

    output = Path(args.output) if args.output else None

    if args.source == "telco":
        import_telco(output)
    else:
        if not args.input:
            parser.error("--input is required when --source file")
        import_custom_csv(Path(args.input), output)


if __name__ == "__main__":
    main()
