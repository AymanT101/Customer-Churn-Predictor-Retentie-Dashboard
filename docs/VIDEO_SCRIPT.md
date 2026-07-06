# Video Script — Customer Churn Predictor & Retentie Dashboard

**Doel:** Portfolio-demo (~2:30 min)  
**Taal:** Nederlands (voice-over)  
**Tone:** Professioneel, concreet, business-first  
**Opname:** Schermopname dashboard + korte API-docs cutaway

---

## Pre-productie checklist

- [ ] Dashboard draait lokaal of op Render (`http://localhost:8501`)
- [ ] API draait (`http://localhost:8000/docs`) — optioneel, 10 sec cutaway
- [ ] Filters staan op Medium / High / Critical
- [ ] Zoom browser op 110%, dark mode uit, geen persoonlijke tabs zichtbaar
- [ ] Cursor langzaam bewegen; 2–3 sec pauze per actie

---

## Script

### Scene 1 — Hook (0:00 – 0:20)

**Beeld:** Dashboard homepage, KPI-kaarten zichtbaar.

**Voice-over:**
> "Als B2B SaaS-bedrijf verlies je elke maand klanten — en daarmee recurring revenue.  
> Het probleem: je weet vaak te laat wie dreigt op te zeggen.  
> Dit project lost dat op: een ML-model dat churn voorspelt, een API voor integratie,  
> en een dashboard waar customer success direct kan handelen."

**Actie:** Geen klikken. Laat KPI's (At-risk klanten, MRR at risk) even in beeld.

---

### Scene 2 — Business KPI's (0:20 – 0:45)

**Beeld:** Tab **Overzicht**, focus op de vijf KPI-kaarten.

**Voice-over:**
> "Bovenaan zie je meteen de business impact: hoeveel klanten at-risk zijn,  
> hoeveel kritiek risico hebben, en — cruciaal — hoeveel MRR op het spel staat.  
> Geen abstract model-score, maar metrics die een CSM-team morgen kan gebruiken."

**Actie:** Hover over **MRR at risk** en **Kritiek risico**.

---

### Scene 3 — Visualisaties (0:45 – 1:10)

**Beeld:** Scroll naar charts: risicoverdeling, scatter, plan/MRR.

**Voice-over:**
> "De visualisaties laten patronen zien: welke plannen het meest risico lopen,  
> en hoe churn-kans samenhangt met tenure en MRR.  
> Bubble-grootte is omzet — zo zie je direct waar je focus moet liggen."

**Actie:** Hover op een paar bubbles in de scatter; kort plan-tier chart highlighten.

---

### Scene 4 — Prioriteitenlijst (1:10 – 1:35)

**Beeld:** Tab **At-risk klanten**.

**Voice-over:**
> "De prioriteitenlijst sorteert klanten op churn-kans.  
> Customer success kan filteren op risiconiveau, plan en minimum MRR —  
> zodat het team eerst de klanten pakt met de hoogste impact."

**Actie:**
1. Sidebar: verhoog **Min. MRR** slider licht
2. Toon gefilterde tabel met progress bars

---

### Scene 5 — Klantdetail & acties (1:35 – 2:00)

**Beeld:** Tab **Klantdetail**.

**Voice-over:**
> "Per klant zie je risicosignalen en concrete actie-adviezen —  
> van een product walkthrough tot een renewal-gesprek.  
> Geen black box: het model vertaalt features naar begrijpelijke signalen."

**Actie:** Selecteer een klant met hoog risico (Critical/High).  
Toon risicosignalen + aanbevolen acties + engagement-radar.

---

### Scene 6 — Tech stack cutaway (2:00 – 2:15)

**Beeld:** Snel wisselen: FastAPI `/docs` → GitHub repo structuur (optioneel) → sidebar model metrics.

**Voice-over:**
> "Onder de motorkap: XGBoost met een scikit-learn preprocessing pipeline,  
> een FastAPI-service voor realtime voorspellingen, en Streamlit voor het dashboard.  
> Alles containerized en deploybaar via Docker en Render."

**Actie:** Open `/docs`, klik kort op `POST /predict`. Toon ROC-AUC in sidebar.

---

### Scene 7 — Close (2:15 – 2:30)

**Beeld:** Terug naar dashboard overview, volledig scherm.

**Voice-over:**
> "Ik bouw systemen die voortijdig signaleren welke klanten weglopen —  
> inclusief API, ML-pipeline en een dashboard waarmee customer success direct kan handelen.  
> Link naar de live demo en repo staan in de beschrijving."

**Actie:** Fade out of eindkaart met GitHub + live demo URL.

---

## B-roll suggesties (optioneel)

| Clip | Duur | Doel |
|------|------|------|
| Terminal: `python -m src.models.train` | 5 sec | ML-credibility |
| Docker Compose start | 5 sec | DevOps |
| `curl` naar `/predict` | 5 sec | API-first |

---

## Eindkaart (overlay tekst)

```
Customer Churn Predictor & Retentie Dashboard
─────────────────────────────────────────────
🔗 Live demo: [Render dashboard URL]
💻 GitHub:    [repo URL]
📧 Contact:   [jouw e-mail / LinkedIn]
```

---

## Variant: korte versie (60 sec)

1. **0–10s** Hook + KPI's  
2. **10–25s** Prioriteitenlijst scroll  
3. **25–40s** Klantdetail met acties  
4. **40–50s** API docs flash + model metrics  
5. **50–60s** Close + links
