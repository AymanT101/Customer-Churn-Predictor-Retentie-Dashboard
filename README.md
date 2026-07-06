# Customer Churn Predictor & Retentie Dashboard

B2B SaaS portfolio project: voorspel welke klanten waarschijnlijk churnen en geef het customer success team een actiegericht dashboard.

## Wat dit project laat zien

- **Business impact**: MRR at risk, prioriteitenlijst en concrete retentie-acties
- **ML engineering**: XGBoost-model met preprocessing pipeline en model persistence
- **API-first**: FastAPI voor realtime voorspellingen (single + batch)
- **Product-ready UX**: Streamlit dashboard met filters, KPI's en klantdetail
- **Deploybaar**: Docker Compose voor lokale demo of portfolio-deploy

## Tech stack

| Component | Technologie |
|-----------|-------------|
| ML | scikit-learn, XGBoost |
| API | FastAPI + Uvicorn |
| Dashboard | Streamlit + Plotly |
| Infra | Docker, Docker Compose |

## Projectstructuur

```
├── src/
│   ├── api/           # FastAPI prediction service
│   ├── dashboard/     # Streamlit retention dashboard
│   ├── data/          # Synthetic data generator
│   └── models/        # Training & inference
├── data/raw/          # Customer CSV
├── models/artifacts/  # Trained model + metrics
├── docker-compose.yml
└── requirements.txt
```

## Snel starten (lokaal)

```bash
# 1. Virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 2. Dependencies
pip install -r requirements.txt

# 3. Data genereren + model trainen
python -m src.data.generate_data
python -m src.models.train

# 4. API starten (terminal 1)
uvicorn src.api.main:app --reload --port 8000

# 5. Dashboard starten (terminal 2)
streamlit run src/dashboard/app.py
```

- **API docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

## Docker

```bash
docker compose up --build
```

Dashboard: http://localhost:8501 · API: http://localhost:8000

Model artifacts and customer data are stored in **named Docker volumes** (`model_artifacts`, `customer_data`) so empty host bind mounts cannot overwrite a trained model. On first startup the API auto-generates data and trains when no model is present.

## API voorbeelden

**Health check**
```bash
curl http://localhost:8000/health
```

**Single prediction**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-9999",
    "company_name": "Demo BV",
    "tenure_months": 4,
    "mrr_eur": 499,
    "seats": 15,
    "plan_tier": "Professional",
    "industry": "SaaS",
    "payment_method": "Invoice",
    "onboarding_completed": "No",
    "login_days_last_30": 2,
    "support_tickets_last_90": 7,
    "feature_adoption_pct": 22,
    "nps_score": 5,
    "days_since_last_login": 18,
    "contract_months_remaining": 1
  }'
```

## Dashboard features

- **KPI-overzicht**: at-risk klanten, kritiek risico, MRR at risk
- **Visualisaties**: risicoverdeling, churn vs tenure, plan/MRR-segmenten
- **Prioriteitenlijst**: sorteerbare tabel met churn-scores
- **Klantdetail**: risicosignalen + aanbevolen CS-acties per klant

## Model features

| Feature | Beschrijving |
|---------|--------------|
| `tenure_months` | Hoe lang klant al klant is |
| `mrr_eur` | Monthly recurring revenue |
| `login_days_last_30` | Actieve dagen afgelopen maand |
| `support_tickets_last_90` | Supportvolume |
| `feature_adoption_pct` | % features in gebruik |
| `nps_score` | Net Promoter Score |
| `days_since_last_login` | Recency |
| `contract_months_remaining` | Renewal timing |

## Portfolio pitch

> *"Ik bouw systemen die voortijdig signaleren welke klanten weglopen — inclusief API, ML-pipeline en een dashboard waarmee customer success direct kan handelen."*

## Licentie

MIT — vrij te gebruiken in je portfolio.
