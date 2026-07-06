# Dataset — synthetisch, Telco of eigen CSV

## Optie 1: Synthetische data (default)

```bash
python -m src.data.generate_data
python -m src.models.train
```

Genereert 2.500 B2B SaaS-klanten met realistische churn-signalen.

## Optie 2: Echte publieke data (IBM Telco)

Downloadt ~7.000 echte telecom-klanten en mapt ze naar het B2B SaaS-schema:

```bash
python -m src.data.import_real --source telco
python -m src.models.train
```

Bron: [IBM Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-ibm) (publiek, geen account nodig).

## Optie 3: Jouw eigen CSV

Je CSV moet deze kolommen bevatten:

| Kolom | Type | Voorbeeld |
|-------|------|-----------|
| `customer_id` | string | `CUST-1001` |
| `company_name` | string | `Acme BV` |
| `tenure_months` | int | `18` |
| `mrr_eur` | float | `499.0` |
| `seats` | int | `25` |
| `plan_tier` | Starter / Professional / Enterprise | `Professional` |
| `industry` | SaaS, FinTech, Healthcare, Retail, Manufacturing, Education | `SaaS` |
| `payment_method` | Credit Card, Invoice, SEPA | `Invoice` |
| `onboarding_completed` | Yes / No | `Yes` |
| `login_days_last_30` | int 0–31 | `12` |
| `support_tickets_last_90` | int | `3` |
| `feature_adoption_pct` | float 0–100 | `62.5` |
| `nps_score` | int 0–10 | `8` |
| `days_since_last_login` | int | `4` |
| `contract_months_remaining` | int | `10` |
| `churned` | 0 of 1 | `1` |

Import:

```bash
python -m src.data.import_real --source file --input pad/naar/jouw_klanten.csv
python -m src.models.train
```

## Tips voor je eigen data

- **Geen gevoelige PII in Git** — `data/raw/*.csv` staat in `.gitignore`
- **Churn-label** — `churned=1` als klant is opgezegd, anders `0`
- **MRR** — gebruik maandelijkse recurring revenue; bij jaarcontract: deel door 12
- **Ontbrekende kolommen** — map in Excel/SQL naar bovenstaand schema vóór import
