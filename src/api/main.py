"""FastAPI service for churn predictions."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import METRICS_PATH, MODEL_PATH
from src.models.bootstrap import ensure_model_artifacts
from src.models.predict import predict_churn


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_model_artifacts()
    yield


app = FastAPI(
    title="Churn Predictor API",
    description="B2B SaaS customer churn prediction service",
    version="1.0.0",
    lifespan=lifespan,
)


class CustomerFeatures(BaseModel):
    customer_id: str = Field(..., examples=["CUST-1001"])
    company_name: str = Field(..., examples=["Acme Corp"])
    tenure_months: int = Field(..., ge=0, examples=[18])
    mrr_eur: float = Field(..., ge=0, examples=[499.0])
    seats: int = Field(..., ge=1, examples=[25])
    plan_tier: Literal["Starter", "Professional", "Enterprise"] = "Professional"
    industry: Literal["SaaS", "FinTech", "Healthcare", "Retail", "Manufacturing", "Education"] = "SaaS"
    payment_method: Literal["Credit Card", "Invoice", "SEPA"] = "Credit Card"
    onboarding_completed: Literal["Yes", "No"] = "Yes"
    login_days_last_30: int = Field(..., ge=0, le=31, examples=[12])
    support_tickets_last_90: int = Field(..., ge=0, examples=[3])
    feature_adoption_pct: float = Field(..., ge=0, le=100, examples=[62.5])
    nps_score: int = Field(..., ge=0, le=10, examples=[8])
    days_since_last_login: int = Field(..., ge=0, examples=[4])
    contract_months_remaining: int = Field(..., ge=0, examples=[10])


class PredictionResponse(BaseModel):
    customer_id: str
    company_name: str
    churn_probability: float
    churn_prediction: int
    risk_level: str
    risk_factors: list[str]


class BatchPredictionRequest(BaseModel):
    customers: list[CustomerFeatures]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
    count: int


@app.get("/health")
def health():
    model_ready = MODEL_PATH.exists()
    return {
        "status": "ok" if model_ready else "degraded",
        "model_loaded": model_ready,
    }


@app.get("/metrics")
def metrics():
    if not METRICS_PATH.exists():
        raise HTTPException(status_code=404, detail="Model metrics not available. Train the model first.")
    import json

    return json.loads(METRICS_PATH.read_text())


@app.post("/predict", response_model=PredictionResponse)
def predict_single(customer: CustomerFeatures):
    try:
        df = pd.DataFrame([customer.model_dump()])
        result = predict_churn(df).iloc[0]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PredictionResponse(
        customer_id=result["customer_id"],
        company_name=result["company_name"],
        churn_probability=float(result["churn_probability"]),
        churn_prediction=int(result["churn_prediction"]),
        risk_level=result["risk_level"],
        risk_factors=result["risk_factors"],
    )


@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest):
    if not request.customers:
        raise HTTPException(status_code=400, detail="No customers provided")

    try:
        df = pd.DataFrame([c.model_dump() for c in request.customers])
        results = predict_churn(df)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    predictions = [
        PredictionResponse(
            customer_id=row["customer_id"],
            company_name=row["company_name"],
            churn_probability=float(row["churn_probability"]),
            churn_prediction=int(row["churn_prediction"]),
            risk_level=row["risk_level"],
            risk_factors=row["risk_factors"],
        )
        for _, row in results.iterrows()
    ]
    return BatchPredictionResponse(predictions=predictions, count=len(predictions))
