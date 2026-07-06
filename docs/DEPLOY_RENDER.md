# Deploy op Render

Gratis hosting voor portfolio-demo: API + Streamlit dashboard als twee web services.

## Snelste route (Blueprint)

1. Push deze repo naar GitHub.
2. Ga naar [Render Blueprints](https://dashboard.render.com/blueprints).
3. **New Blueprint Instance** → selecteer de repo.
4. Render leest `render.yaml` en maakt **churn-api** en **churn-dashboard** aan.
5. Wacht tot beide services **Live** zijn (eerste deploy ~5–10 min; model traint automatisch bij startup).

**Dashboard-URL:** `https://churn-dashboard.onrender.com` (naam kan afwijken)  
**API-URL:** `https://churn-api.onrender.com`

## Wat gebeurt er bij startup?

1. **API** — `ensure_model_artifacts()` genereert data (synthetisch) en traint XGBoost als er nog geen model is.
2. **Dashboard** — leest klantdata en roept de API aan voor batch-voorspellingen (`USE_API=true`).

> Op de free tier kan de eerste request 30–60 sec duren (cold start). Daarna is het sneller.

## Echte dataset gebruiken op Render

Render free tier heeft **geen persistent disk**. Bij elke redeploy start je opnieuw met synthetische data.

Opties:

| Optie | Wanneer |
|-------|---------|
| Synthetisch (default) | Snelle demo, geen extra stappen |
| Telco dataset in repo | Commit `data/raw/customers.csv` na lokaal importeren (alleen als je geen gevoelige data deelt) |
| Render Disk (paid) | Persistente CSV + model artifacts |

Lokaal Telco importeren en model trainen:

```bash
python -m src.data.import_real --source telco
python -m src.models.train
```

## Handmatig deployen (zonder Blueprint)

### API service

- **Runtime:** Docker
- **Dockerfile:** `Dockerfile.api`
- **Health check path:** `/health`

### Dashboard service

- **Runtime:** Docker
- **Dockerfile:** `Dockerfile.dashboard`
- **Environment variables:**

| Key | Value |
|-----|-------|
| `USE_API` | `true` |
| `API_URL` | `https://<jouw-api-service>.onrender.com` |

## Troubleshooting

| Probleem | Oplossing |
|----------|-----------|
| Dashboard toont "API niet bereikbaar" | Controleer `API_URL`; API moet Live zijn |
| Lange laadtijd | Free tier cold start; refresh na ~60 sec |
| Health check faalt | API training duurt ~60 sec; `start_period` in Docker healthcheck is 90s |
| Oude voorspellingen | Redeploy dashboard; geen persistent cache op free tier |
