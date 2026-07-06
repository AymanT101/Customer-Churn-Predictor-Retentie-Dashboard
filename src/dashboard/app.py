"""Streamlit retention dashboard for customer success teams."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

from src.config import METRICS_PATH, RAW_DATA_PATH, RISK_THRESHOLDS
from src.models.predict import predict_churn

API_URL = os.getenv("API_URL", "http://localhost:8000")
USE_API = os.getenv("USE_API", "false").lower() == "true"

RISK_COLORS = {
    "Low": "#22c55e",
    "Medium": "#eab308",
    "High": "#f97316",
    "Critical": "#ef4444",
}

st.set_page_config(
    page_title="Retentie Dashboard | Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Klantdata laden...")
def load_customers() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        from src.data.generate_data import main as generate_data

        generate_data()
    return pd.read_csv(RAW_DATA_PATH)


@st.cache_data(show_spinner="Churn-scores berekenen...")
def load_predictions(_data_version: str) -> pd.DataFrame:
    customers = load_customers()
    if USE_API:
        try:
            payload = {"customers": customers.to_dict(orient="records")}
            response = requests.post(f"{API_URL}/predict/batch", json=payload, timeout=60)
            response.raise_for_status()
            preds = response.json()["predictions"]
            pred_df = pd.DataFrame(preds)
            return customers.merge(
                pred_df[
                    [
                        "customer_id",
                        "churn_probability",
                        "churn_prediction",
                        "risk_level",
                        "risk_factors",
                    ]
                ],
                on="customer_id",
            )
        except requests.RequestException:
            st.warning("API niet bereikbaar — voorspellingen lokaal berekend.")
    return predict_churn(customers)


@st.cache_data
def load_model_metrics() -> dict | None:
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text())
    return None


def format_eur(value: float) -> str:
    return f"€{value:,.0f}".replace(",", ".")


def render_kpis(df: pd.DataFrame) -> None:
    total = len(df)
    at_risk = (df["churn_probability"] >= RISK_THRESHOLDS["low"]).sum()
    critical = (df["risk_level"] == "Critical").sum()
    mrr_at_risk = df.loc[df["churn_probability"] >= RISK_THRESHOLDS["medium"], "mrr_eur"].sum()
    avg_prob = df["churn_probability"].mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Totaal klanten", f"{total:,}".replace(",", "."))
    c2.metric("At-risk klanten", at_risk, delta=f"{at_risk / total * 100:.1f}%", delta_color="inverse")
    c3.metric("Kritiek risico", critical, delta="Direct actie", delta_color="inverse")
    c4.metric("MRR at risk", format_eur(mrr_at_risk))
    c5.metric("Gem. churn-kans", f"{avg_prob:.1f}%")


def render_charts(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)

    with col1:
        risk_counts = df["risk_level"].value_counts().reindex(
            ["Low", "Medium", "High", "Critical"], fill_value=0
        )
        fig_risk = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            labels={"x": "Risiconiveau", "y": "Aantal klanten"},
            title="Klanten per risiconiveau",
            color=risk_counts.index,
            color_discrete_map=RISK_COLORS,
        )
        fig_risk.update_layout(showlegend=False, height=360)
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        scatter_df = df.copy()
        scatter_df["mrr_eur"] = scatter_df["mrr_eur"].clip(upper=scatter_df["mrr_eur"].quantile(0.95))
        fig_scatter = px.scatter(
            scatter_df,
            x="tenure_months",
            y="churn_probability",
            size="mrr_eur",
            color="risk_level",
            hover_data=["company_name", "mrr_eur", "plan_tier"],
            color_discrete_map=RISK_COLORS,
            labels={
                "tenure_months": "Tenure (maanden)",
                "churn_probability": "Churn-kans",
            },
            title="Churn-kans vs. klantleeftijd (bubble = MRR)",
        )
        fig_scatter.update_layout(height=360)
        st.plotly_chart(fig_scatter, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        plan_risk = (
            df.groupby("plan_tier")["churn_probability"]
            .mean()
            .reset_index()
            .sort_values("churn_probability", ascending=False)
        )
        fig_plan = px.bar(
            plan_risk,
            x="plan_tier",
            y="churn_probability",
            title="Gemiddelde churn-kans per plan",
            labels={"plan_tier": "Plan", "churn_probability": "Gem. churn-kans"},
            color="plan_tier",
        )
        fig_plan.update_layout(showlegend=False, height=320)
        st.plotly_chart(fig_plan, use_container_width=True)

    with col4:
        mrr_bins = pd.cut(
            df["mrr_eur"],
            bins=[0, 200, 500, 1000, 5000, 100000],
            labels=["<€200", "€200-500", "€500-1K", "€1K-5K", ">€5K"],
        )
        mrr_risk = df.groupby(mrr_bins, observed=True)["churn_probability"].mean().reset_index()
        mrr_risk.columns = ["mrr_segment", "churn_probability"]
        fig_mrr = px.line(
            mrr_risk,
            x="mrr_segment",
            y="churn_probability",
            markers=True,
            title="Churn-kans per MRR-segment",
            labels={"mrr_segment": "MRR-segment", "churn_probability": "Gem. churn-kans"},
        )
        fig_mrr.update_layout(height=320)
        st.plotly_chart(fig_mrr, use_container_width=True)


def render_customer_table(df: pd.DataFrame) -> None:
    display = df[
        [
            "customer_id",
            "company_name",
            "plan_tier",
            "mrr_eur",
            "tenure_months",
            "churn_probability",
            "risk_level",
            "nps_score",
            "login_days_last_30",
            "support_tickets_last_90",
        ]
    ].copy()
    display["churn_probability"] = (display["churn_probability"] * 100).round(1)
    display = display.rename(
        columns={
            "customer_id": "ID",
            "company_name": "Bedrijf",
            "plan_tier": "Plan",
            "mrr_eur": "MRR (€)",
            "tenure_months": "Tenure",
            "churn_probability": "Churn %",
            "risk_level": "Risico",
            "nps_score": "NPS",
            "login_days_last_30": "Logins (30d)",
            "support_tickets_last_90": "Tickets (90d)",
        }
    )
    st.dataframe(
        display.sort_values("Churn %", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Churn %": st.column_config.ProgressColumn(
                "Churn %",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "MRR (€)": st.column_config.NumberColumn(format="€%.0f"),
        },
    )


def render_customer_detail(df: pd.DataFrame) -> None:
    st.subheader("Klantdetail & actie-advies")
    options = df.sort_values("churn_probability", ascending=False)["company_name"].tolist()
    selected = st.selectbox("Selecteer klant", options)

    row = df[df["company_name"] == selected].iloc[0]
    prob_pct = row["churn_probability"] * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Churn-kans", f"{prob_pct:.1f}%")
    c2.metric("MRR", format_eur(row["mrr_eur"]))
    c3.metric("Risiconiveau", row["risk_level"])

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("**Risicosignalen**")
        for factor in row["risk_factors"]:
            st.markdown(f"- {factor}")

        st.markdown("**Aanbevolen acties**")
        actions = []
        if row["login_days_last_30"] < 8:
            actions.append("Plan een product walkthrough of training sessie")
        if row["support_tickets_last_90"] >= 5:
            actions.append("Escalatie naar senior CSM — analyseer ticketpatroon")
        if row["nps_score"] <= 6:
            actions.append("Voer een satisfaction call uit binnen 48 uur")
        if row["contract_months_remaining"] <= 2:
            actions.append("Start renewal-gesprek met waarde-demonstratie")
        if row["feature_adoption_pct"] < 40:
            actions.append("Stuur gepersonaliseerde onboarding-flow voor underused features")
        if not actions:
            actions.append("Monitor — geen urgente interventie nodig")
        for action in actions:
            st.markdown(f"- ✅ {action}")

    with col_b:
        metrics = {
            "Logins (30d)": row["login_days_last_30"],
            "Tickets (90d)": row["support_tickets_last_90"],
            "Feature adoptie %": row["feature_adoption_pct"],
            "NPS": row["nps_score"],
            "Dagen sinds login": row["days_since_last_login"],
            "Contract resterend (mnd)": row["contract_months_remaining"],
        }
        fig = go.Figure(
            go.Scatterpolar(
                r=[
                    min(row["login_days_last_30"] / 30 * 100, 100),
                    max(100 - row["support_tickets_last_90"] * 10, 0),
                    row["feature_adoption_pct"],
                    row["nps_score"] * 10,
                    max(100 - row["days_since_last_login"] * 3, 0),
                    min(row["contract_months_remaining"] / 12 * 100, 100),
                ],
                theta=list(metrics.keys()),
                fill="toself",
                name=row["company_name"],
            )
        )
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Engagement-profiel",
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.title("📊 Customer Churn Predictor & Retentie Dashboard")
    st.caption(
        "Voorspel welke B2B-klanten dreigen op te zeggen — "
        "zodat je customer success team proactief kan ingrijpen."
    )

    customers = load_customers()
    data_version = f"{len(customers)}-{customers['customer_id'].iloc[-1]}"
    df = load_predictions(data_version)

    with st.sidebar:
        st.header("Filters")
        risk_filter = st.multiselect(
            "Risiconiveau",
            options=["Low", "Medium", "High", "Critical"],
            default=["Medium", "High", "Critical"],
        )
        plan_filter = st.multiselect(
            "Plan",
            options=sorted(df["plan_tier"].unique()),
            default=sorted(df["plan_tier"].unique()),
        )
        min_mrr = st.slider("Min. MRR (€)", 0, int(df["mrr_eur"].max()), 0)
        min_prob = st.slider("Min. churn-kans (%)", 0, 100, 20) / 100

        st.divider()
        st.markdown("**Modelprestaties**")
        metrics = load_model_metrics()
        if metrics:
            st.metric("ROC-AUC", metrics.get("roc_auc", "—"))
            st.metric("Recall", metrics.get("recall", "—"))
            st.metric("F1-score", metrics.get("f1", "—"))
        else:
            st.info("Train het model om metrics te zien.")

        st.divider()
        st.caption(f"Data: {len(customers):,} klanten".replace(",", "."))

    filtered = df[
        (df["risk_level"].isin(risk_filter))
        & (df["plan_tier"].isin(plan_filter))
        & (df["mrr_eur"] >= min_mrr)
        & (df["churn_probability"] >= min_prob)
    ]

    tab_overview, tab_customers, tab_detail = st.tabs(
        ["Overzicht", "At-risk klanten", "Klantdetail"]
    )

    with tab_overview:
        render_kpis(filtered)
        st.divider()
        render_charts(filtered)

    with tab_customers:
        st.subheader(f"Prioriteitenlijst ({len(filtered)} klanten)")
        render_customer_table(filtered)

    with tab_detail:
        detail_df = filtered if len(filtered) > 0 else df
        render_customer_detail(detail_df)


if __name__ == "__main__":
    main()
