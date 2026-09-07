"""Render the S2 four-card decision KPI strip."""

import pandas as pd
import streamlit as st


def _pct(value: float) -> str:
    return f"{value:+.1f}%"


def _cr(value: float) -> str:
    return f"₹{value:.1f} Cr"


def render(summary: pd.Series) -> None:
    """Render reported, verified, headroom, and data-quality cards."""
    reported = float(summary["reported_change_pct"])
    verified = float(summary["verified_change_pct"])
    headroom = reported - verified
    cards = [
        ("REPORTED", _pct(reported), "legacy definition, uncorrected", "legacy"),
        ("VERIFIED", _pct(verified), f"95% CI: {_pct(float(summary['verified_ci_low']))} to {_pct(float(summary['verified_ci_high']))}", "hero"),
        ("HEADROOM", f"{headroom:.1f} pts", "unexplained by operations", ""),
        ("DATA QUALITY", f"{int(summary['dq_issues_count'])} issues · {_cr(float(summary['dq_adjustment_cr']))} adjusted", "see DQ report", ""),
    ]
    html = '<div class="kpi-grid">'
    for label, value, note, variant in cards:
        html += f'<div class="kpi-card {variant}"><div class="kpi-label">{label}</div><div class="kpi-value {"legacy" if label == "REPORTED" else ""}">{value}</div><div class="kpi-note">{note}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
