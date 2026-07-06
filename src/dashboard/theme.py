"""Monochrome glassmorphism theme for the Streamlit dashboard."""

from __future__ import annotations

import streamlit as st

AUTHOR_NAME = "Ayman Thomas"

# Risk levels mapped to grayscale (light → critical)
RISK_COLORS = {
    "Low": "#525252",
    "Medium": "#737373",
    "High": "#A3A3A3",
    "Critical": "#E5E5E5",
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
        tickfont=dict(color="#D4D4D4"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.15)",
        zerolinecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#D4D4D4"),
    ),
    legend=dict(bgcolor="rgba(255,255,255,0.04)", bordercolor="rgba(255,255,255,0.1)"),
    margin=dict(l=24, r=24, t=48, b=24),
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --text-primary: #F5F5F5;
    --text-secondary: #CFCFCF;
    --text-muted: #9CA3AF;
    --glass-bg: rgba(18, 18, 18, 0.72);
    --glass-border: rgba(255, 255, 255, 0.12);
}

html, body {
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--text-primary);
    background: #050505;
    overflow-x: hidden;
    overflow-y: auto;
    height: auto;
    min-height: 100%;
}

.stApp {
    background: #050505;
    color: var(--text-primary);
    overflow-x: hidden;
    overflow-y: auto !important;
    min-height: 100vh;
    height: auto;
}

[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
    background: transparent;
    overflow: visible !important;
    min-height: 100vh;
    height: auto;
}

[data-testid="stMain"] {
    overflow: visible !important;
    height: auto;
}

section.main {
    position: relative;
    z-index: 1;
    background: transparent;
    overflow: visible !important;
    height: auto !important;
    min-height: 100vh;
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
    animation: fadeUp 0.6s ease-out;
    overflow: visible;
}

/* Background orbs on body — not on .stApp (avoids scroll trap) */
body::before,
body::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.12;
    z-index: 0;
    pointer-events: none;
    animation: floatOrb 20s ease-in-out infinite;
}

body::before {
    width: 380px;
    height: 380px;
    top: -100px;
    right: -60px;
    background: radial-gradient(circle, rgba(255,255,255,0.25) 0%, transparent 70%);
}

body::after {
    width: 320px;
    height: 320px;
    bottom: -80px;
    left: -40px;
    background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, transparent 70%);
    animation-delay: -10s;
}

@keyframes floatOrb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(20px, -15px) scale(1.03); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Global text readability (fix invisible / white-on-white text) ── */
.stApp p, .stApp span, .stApp li, .stApp label,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] span,
.stApp [data-testid="stMarkdownContainer"] strong,
.stApp [data-testid="stCaptionContainer"] p {
    color: var(--text-secondary) !important;
}

.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3 {
    color: var(--text-primary) !important;
}

.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
}

.stApp .stSlider label {
    color: var(--text-muted) !important;
}

.stApp [data-testid="stAlert"] p,
.stApp [data-testid="stAlert"] span {
    color: #E5E5E5 !important;
}

.stApp [data-testid="stAlert"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #E5E5E5 !important;
}

/* Select / multiselect chips */
.stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="tag"] {
    background-color: rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
    border-color: rgba(255,255,255,0.15) !important;
}

.stApp input, .stApp textarea {
    color: var(--text-primary) !important;
    background-color: rgba(255,255,255,0.06) !important;
}

/* Hero */
.hero-glass {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    animation: fadeUp 0.7s ease-out 0.1s both;
}

.hero-glass h1 {
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #FFFFFF !important;
    margin: 0 0 0.35rem 0;
}

.hero-glass p {
    color: #B8B8B8 !important;
    margin: 0;
    font-size: 0.95rem;
}

.hero-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem;
    margin-top: 0.85rem;
}

.hero-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.hero-author {
    font-size: 0.78rem;
    color: #A3A3A3 !important;
    letter-spacing: 0.02em;
}

.hero-author strong {
    color: #FFFFFF !important;
    font-weight: 600;
}

/* Glass panels */
.glass-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1rem 1.15rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.25s ease, transform 0.25s ease;
    animation: fadeUp 0.55s ease-out both;
}

.glass-panel:hover {
    border-color: rgba(255, 255, 255, 0.2);
}

.glass-panel-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #9CA3AF !important;
    margin-bottom: 0.35rem;
}

.glass-panel-value {
    font-size: 1.65rem;
    font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -0.02em;
}

.glass-panel-delta {
    font-size: 0.78rem;
    color: #A3A3A3 !important;
    margin-top: 0.15rem;
}

.glass-panel h4 {
    color: #FFFFFF !important;
    font-size: 0.95rem;
    margin: 0 0 0.65rem 0;
}

.glass-panel ul {
    margin: 0;
    padding-left: 1.1rem;
}

.glass-panel li {
    color: #D4D4D4 !important;
    margin-bottom: 0.35rem;
    line-height: 1.45;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(8, 8, 8, 0.92) !important;
    backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] .block-container {
    animation: none;
}

.sidebar-brand {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #737373 !important;
    margin-bottom: 0.5rem;
}

.sidebar-author {
    margin-top: 1.5rem;
    padding: 0.85rem 1rem;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
}

.sidebar-author p {
    margin: 0 !important;
    font-size: 0.72rem !important;
    color: #737373 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.sidebar-author strong {
    display: block;
    margin-top: 0.25rem;
    font-size: 0.95rem !important;
    color: #FFFFFF !important;
    letter-spacing: 0.01em;
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
    color: #737373 !important;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: rgba(255, 255, 255, 0.1) !important;
    color: #FFFFFF !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 0.85rem 1rem;
}

[data-testid="stMetricLabel"] {
    color: #9CA3AF !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Circle spinner */
div[data-testid="stSpinner"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.75rem !important;
}

div[data-testid="stSpinner"] svg {
    display: none !important;
}

div[data-testid="stSpinner"]::before {
    content: "";
    width: 44px;
    height: 44px;
    border: 2px solid rgba(255,255,255,0.12);
    border-top-color: #FFFFFF;
    border-radius: 50%;
    animation: spin 0.75s linear infinite;
}

div[data-testid="stSpinner"] p {
    color: #9CA3AF !important;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Charts */
.chart-glass {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 0.5rem 0.75rem 0.25rem;
    margin-bottom: 0.5rem;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stDataFrame"] [data-testid="glideDataEditor"],
[data-testid="stDataFrame"] canvas {
    background: #0A0A0A !important;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #FFFFFF !important;
    margin: 0.5rem 0 1rem;
}

/* Footer credit */
.site-footer {
    margin-top: 2.5rem;
    padding: 1rem 0 0.5rem;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.08);
    animation: fadeUp 0.6s ease-out 0.3s both;
}

.site-footer p {
    margin: 0 !important;
    font-size: 0.78rem !important;
    color: #737373 !important;
    letter-spacing: 0.04em;
}

.site-footer .author-name {
    color: #FFFFFF !important;
    font-weight: 600;
}

#MainMenu {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    height: 0;
    min-height: 0;
    overflow: hidden;
    visibility: hidden;
    pointer-events: none;
}

footer {
    visibility: hidden;
    height: 0;
    min-height: 0;
    overflow: hidden;
}

hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
}
</style>
"""


def inject_theme() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-glass">
            <h1>Customer Churn Predictor</h1>
            <p>Retentie dashboard voor customer success — voorspel churn, prioriteer acties, bescherm MRR.</p>
            <div class="hero-meta">
                <span class="hero-badge">ML · API · Glass UI</span>
                <span class="hero-author">Made by <strong>{AUTHOR_NAME}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_author_sidebar() -> None:
    st.markdown(
        f"""
        <div class="sidebar-author">
            <p>Made by</p>
            <strong>{AUTHOR_NAME}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="site-footer">
            <p>Made by <span class="author-name">{AUTHOR_NAME}</span></p>
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


def glass_text_block(title: str, items: list[str]) -> str:
    list_html = "".join(f"<li>{item}</li>" for item in items)
    return f"""
    <div class="glass-panel">
        <h4>{title}</h4>
        <ul>{list_html}</ul>
    </div>
    """
