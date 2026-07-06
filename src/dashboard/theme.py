"""Monochrome glassmorphism theme for the Streamlit dashboard."""

from __future__ import annotations

import streamlit as st

# Risk levels mapped to grayscale (light → critical)
RISK_COLORS = {
    "Low": "#737373",
    "Medium": "#A3A3A3",
    "High": "#D4D4D4",
    "Critical": "#FFFFFF",
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
    font=dict(color="#E5E5E5", family="Inter, system-ui, sans-serif", size=12),
    title=dict(font=dict(color="#FFFFFF", size=15)),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.15)",
        zerolinecolor="rgba(255,255,255,0.08)",
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.15)",
        zerolinecolor="rgba(255,255,255,0.08)",
    ),
    legend=dict(bgcolor="rgba(255,255,255,0.04)", bordercolor="rgba(255,255,255,0.1)"),
    margin=dict(l=24, r=24, t=48, b=24),
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif;
}

.stApp {
    background: #050505;
    color: #F5F5F5;
}

/* Animated glass background */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
    animation: floatOrb 18s ease-in-out infinite;
}

.stApp::before {
    width: 420px;
    height: 420px;
    top: -120px;
    right: -80px;
    background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
}

.stApp::after {
    width: 360px;
    height: 360px;
    bottom: -100px;
    left: -60px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
    animation-delay: -9s;
}

@keyframes floatOrb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(30px, -20px) scale(1.05); }
    66% { transform: translate(-20px, 15px) scale(0.95); }
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1.5rem;
    max-width: 1400px;
    animation: fadeUp 0.6s ease-out;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hero header */
.hero-glass {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    animation: fadeUp 0.7s ease-out 0.1s both;
}

.hero-glass h1 {
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #FFFFFF;
    margin: 0 0 0.35rem 0;
}

.hero-glass p {
    color: rgba(255, 255, 255, 0.55);
    margin: 0;
    font-size: 0.95rem;
}

.hero-badge {
    display: inline-block;
    margin-top: 0.85rem;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

/* Glass panels */
.glass-panel {
    background: rgba(255, 255, 255, 0.035);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
    animation: fadeUp 0.55s ease-out both;
}

.glass-panel:hover {
    border-color: rgba(255, 255, 255, 0.18);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    transform: translateY(-2px);
}

.glass-panel-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.45);
    margin-bottom: 0.35rem;
}

.glass-panel-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

.glass-panel-delta {
    font-size: 0.78rem;
    color: rgba(255, 255, 255, 0.5);
    margin-top: 0.15rem;
}

/* Sidebar glass */
[data-testid="stSidebar"] {
    background: rgba(8, 8, 8, 0.85);
    backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] .block-container {
    animation: none;
}

.sidebar-brand {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.35);
    margin-bottom: 0.5rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.5);
    font-weight: 500;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #FFFFFF !important;
}

.stTabs [data-baseweb="tab-panel"] {
    animation: fadeUp 0.4s ease-out;
}

/* Metrics override */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.035);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    transition: border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(255, 255, 255, 0.16);
}

[data-testid="stMetricLabel"] {
    color: rgba(255, 255, 255, 0.45) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Circle loading spinner */
div[data-testid="stSpinner"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.75rem !important;
    padding: 1.5rem !important;
}

div[data-testid="stSpinner"] svg,
div[data-testid="stSpinner"] > div > svg {
    display: none !important;
}

div[data-testid="stSpinner"]::before {
    content: "";
    display: block;
    width: 44px;
    height: 44px;
    border: 2px solid rgba(255, 255, 255, 0.12);
    border-top-color: #FFFFFF;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
}

div[data-testid="stSpinner"] p,
div[data-testid="stSpinner"] span {
    color: rgba(255, 255, 255, 0.55) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Chart wrapper */
.chart-glass {
    background: rgba(255, 255, 255, 0.025);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 0.5rem 0.75rem 0.25rem;
    margin-bottom: 0.5rem;
    animation: fadeUp 0.5s ease-out both;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    overflow: hidden;
}

/* Section headers */
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0.5rem 0 1rem;
    letter-spacing: -0.01em;
}

.risk-pill {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.06);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
    margin: 1.25rem 0 !important;
}
</style>
"""


def inject_theme() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-glass">
            <h1>Customer Churn Predictor</h1>
            <p>Retentie dashboard voor customer success — voorspel churn, prioriteer acties, bescherm MRR.</p>
            <span class="hero-badge">ML · API · Glass UI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_plotly_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig


def glass_kpi(label: str, value: str, delta: str | None = None, delay: float = 0) -> str:
    delta_html = f'<div class="glass-panel-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="glass-panel" style="animation-delay: {delay}s">
        <div class="glass-panel-title">{label}</div>
        <div class="glass-panel-value">{value}</div>
        {delta_html}
    </div>
    """
