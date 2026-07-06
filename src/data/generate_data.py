"""Synthetic B2B SaaS customer dataset generator."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import RAW_DATA_PATH

RNG = np.random.default_rng(42)

PLAN_TIERS = ["Starter", "Professional", "Enterprise"]
INDUSTRIES = ["SaaS", "FinTech", "Healthcare", "Retail", "Manufacturing", "Education"]
PAYMENT_METHODS = ["Credit Card", "Invoice", "SEPA"]
ONBOARDING = ["Yes", "No"]


def _churn_probability(row: pd.Series) -> float:
    """Realistic churn signal based on customer behavior."""
    score = 0.08

    if row["login_days_last_30"] < 5:
        score += 0.35
    elif row["login_days_last_30"] < 12:
        score += 0.15

    if row["support_tickets_last_90"] >= 8:
        score += 0.22
    elif row["support_tickets_last_90"] >= 4:
        score += 0.10

    if row["feature_adoption_pct"] < 30:
        score += 0.25
    elif row["feature_adoption_pct"] < 55:
        score += 0.12

    if row["nps_score"] <= 6:
        score += 0.28
    elif row["nps_score"] <= 8:
        score += 0.08

    if row["days_since_last_login"] > 21:
        score += 0.20
    elif row["days_since_last_login"] > 10:
        score += 0.08

    if row["contract_months_remaining"] <= 1:
        score += 0.18

    if row["tenure_months"] < 6:
        score += 0.12

    if row["plan_tier"] == "Starter":
        score += 0.06

    if row["onboarding_completed"] == "No":
        score += 0.14

    return min(score, 0.95)


def generate_customers(n: int = 2500) -> pd.DataFrame:
    customer_ids = [f"CUST-{1000 + i}" for i in range(n)]
    company_names = [f"Company {i + 1}" for i in range(n)]

    tenure = RNG.integers(1, 72, size=n)
    plan_tier = RNG.choice(PLAN_TIERS, size=n, p=[0.35, 0.45, 0.20])
    industry = RNG.choice(INDUSTRIES, size=n)
    payment_method = RNG.choice(PAYMENT_METHODS, size=n, p=[0.55, 0.30, 0.15])
    onboarding = RNG.choice(ONBOARDING, size=n, p=[0.82, 0.18])

    mrr_base = {"Starter": 149, "Professional": 499, "Enterprise": 1499}
    mrr = np.array([RNG.normal(mrr_base[t], mrr_base[t] * 0.15) for t in plan_tier]).clip(49, 8000)
    seats = RNG.integers(1, 120, size=n)

    login_days = RNG.integers(0, 31, size=n)
    support_tickets = RNG.poisson(2.5, size=n)
    feature_adoption = RNG.beta(2.5, 2.0, size=n) * 100
    nps = RNG.integers(0, 11, size=n)
    days_since_login = RNG.integers(0, 45, size=n)
    contract_remaining = RNG.integers(0, 24, size=n)

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "company_name": company_names,
            "tenure_months": tenure,
            "mrr_eur": np.round(mrr, 2),
            "seats": seats,
            "plan_tier": plan_tier,
            "industry": industry,
            "payment_method": payment_method,
            "onboarding_completed": onboarding,
            "login_days_last_30": login_days,
            "support_tickets_last_90": support_tickets,
            "feature_adoption_pct": np.round(feature_adoption, 1),
            "nps_score": nps,
            "days_since_last_login": days_since_login,
            "contract_months_remaining": contract_remaining,
        }
    )

    churn_probs = df.apply(_churn_probability, axis=1)
    df["churned"] = (RNG.random(n) < churn_probs).astype(int)
    return df


def main(output_path: Path | None = None, n: int = 2500) -> Path:
    path = output_path or RAW_DATA_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_customers(n=n)
    df.to_csv(path, index=False)
    churn_rate = df["churned"].mean() * 100
    print(f"Generated {len(df)} customers -> {path}")
    print(f"Churn rate: {churn_rate:.1f}%")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic B2B SaaS customer data")
    parser.add_argument("--n", type=int, default=2500, help="Number of customers")
    parser.add_argument("--output", type=str, default=None, help="Output CSV path")
    args = parser.parse_args()
    out = Path(args.output) if args.output else None
    main(output_path=out, n=args.n)
