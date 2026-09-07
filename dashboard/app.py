"""Orchestrate the one-screen CEO dashboard from the golden DuckDB contract."""

from pathlib import Path
from datetime import datetime

import streamlit as st

from dashboard.components import counterfactual, header, investment, kpi_strip, trend, truth_table, waterfall
from dashboard.data import load_dashboard_data

ROOT = Path(__file__).parents[1]

st.set_page_config(page_title="Recovery Fact Check", page_icon=":material/search:", layout="wide")

with open(ROOT / "dashboard" / "styles.css", encoding="utf-8") as stylesheet:
    st.html(f"<style>{stylesheet.read()}</style>")

frames, source = load_dashboard_data()
summary = frames["mart_kpi_summary"].iloc[0]
monthly = frames["mart_monthly_trend"].sort_values("month").copy()

with st.sidebar:
    st.markdown("**Source status**")
    source_class = source.lower()
    st.markdown(f'<div class="status-pill {source_class}">{source}</div>', unsafe_allow_html=True)
    st.caption("All displayed values come from the DuckDB mart contract.")
    start_date = monthly["month"].min().date()
    end_date = monthly["month"].max().date()
    date_selection = st.date_input("Date range", value=(start_date, end_date), min_value=start_date, max_value=end_date)
    st.selectbox("Segment", ["All"], index=0, help="The current mart contract is an executive aggregate without a segment dimension.")

if isinstance(date_selection, tuple) and len(date_selection) == 2:
    selected_start, selected_end = date_selection
    monthly = monthly.loc[monthly["month"].dt.date.between(selected_start, selected_end)].copy()

as_of = summary["data_asof_date"].date()
header.render(as_of, source)
st.markdown('<div class="section-label">Verdict</div>', unsafe_allow_html=True)
kpi_strip.render(summary)

st.markdown('<div class="section-label">Proof</div>', unsafe_allow_html=True)
with st.container(border=True):
    waterfall.render(frames["mart_waterfall"].sort_values("component_order"), float(summary["reported_change_pct"]), float(summary["verified_change_pct"]))

trend_column, truth_column = st.columns([1.38, 1], gap="large")
with trend_column:
    st.markdown('<div class="section-title">The reported line diverges from audited recovery</div>', unsafe_allow_html=True)
    trend.render(monthly, float(summary["reported_change_pct"]), float(summary["verified_change_pct"]))
with truth_column:
    st.markdown('<div class="section-title">Six of nine headline metrics need correction</div>', unsafe_allow_html=True)
    truth_table.render(frames["mart_metric_truth"])

st.markdown('<div class="section-label">Cause</div>', unsafe_allow_html=True)
counterfactual.render(frames["mart_counterfactual"].iloc[0])

st.markdown('<div class="section-label">Action</div>', unsafe_allow_html=True)
investment.render(frames["mart_investment"])

generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
st.markdown(f'<div class="footer">Caveats: trailing 45 days provisional (late-arriving payments restated) · channel results under 3 attribution schemes in memo · every number traces to a query in sql/04_metrics/ · Generated {generated_at}.</div>', unsafe_allow_html=True)
