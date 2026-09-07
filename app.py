from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).parent
METRICS = ROOT / "data" / "golden" / "monthly_metrics.csv"
QUALITY = ROOT / "data" / "golden" / "quality_report.json"
st.set_page_config(page_title="Recovery Forensics", page_icon="RF", layout="wide")
st.markdown("""<style>body { background: #f6f3ed; } .block-container { max-width: 1240px; padding-top: 2rem; } h1 { color:#17324d; letter-spacing:0; } .caption { color:#65727e; }</style>""", unsafe_allow_html=True)
st.title("Recovery Forensics")
st.caption("Independent recovery view | fixed month-start denominators | payment-date attribution")
if not METRICS.exists():
    st.error("No golden dataset found. Run: python scripts/generate_demo_data.py, then python -m src.pipeline")
    st.stop()
metrics = pd.read_csv(METRICS, parse_dates=["month"])
quality = json.loads(QUALITY.read_text(encoding="utf-8")) if QUALITY.exists() else {}
latest, prior = metrics.iloc[-1], metrics.iloc[-2]
change = latest.recovery_rate / prior.recovery_rate - 1 if prior.recovery_rate else 0
c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest recovery rate", f"{latest.recovery_rate:.1%}", f"{change:+.1%} MoM")
c2.metric("Settled amount", f"₹{latest.settled_amount:,.0f}")
c3.metric("Recovery / account", f"₹{latest.recovery_per_account:,.0f}")
c4.metric("Eligible accounts", f"{latest.eligible_accounts:,.0f}")
st.divider()
left, right = st.columns([1.7, 1])
with left:
    chart = px.line(metrics, x="month", y=["recovery_rate", "attempt_rate"], markers=True, labels={"value":"Rate", "variable":"Metric", "month":"Month"}, color_discrete_sequence=["#e07a5f", "#2a9d8f"])
    chart.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    st.plotly_chart(chart, use_container_width=True)
with right:
    st.subheader("Data trust")
    st.write(f"Duplicate payment rows removed: **{quality.get('duplicate_payment_rows_removed', 'n/a')}**")
    st.write(f"Metric version: **{quality.get('metric_version', 'n/a')}**")
    st.warning("Demo data only" if quality else "Quality report missing")
st.subheader("Monthly evidence")
st.dataframe(metrics[["month", "eligible_accounts", "recovered_accounts", "settled_amount", "recovery_rate", "recovery_per_account", "reported_mom_change"]], use_container_width=True, hide_index=True)
st.caption("No investment recommendation is valid until real source extracts replace the synthetic demo files and the quality report is reviewed.")
