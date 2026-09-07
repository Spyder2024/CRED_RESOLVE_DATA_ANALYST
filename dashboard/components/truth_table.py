"""Render the S4 metric-truth table with verdict highlighting."""

import html

import pandas as pd
import streamlit as st


def render(truth: pd.DataFrame) -> None:
    """Render the nine metric verdicts without Streamlit's default dataframe chrome."""
    rows = '<div class="truth-table"><div class="truth-row header"><span>Metric</span><span>Reported</span><span>Verified</span><span>Verdict</span></div>'
    for record in truth.itertuples(index=False):
        verdict_class = record.verdict.lower()
        rows += f'<div class="truth-row {verdict_class}"><span title="{html.escape(record.note)}">{html.escape(record.metric_name)}</span><span>{record.reported_change:+.1f}%</span><span>{record.verified_change:+.1f}%</span><span class="verdict"><i class="dot {verdict_class}"></i>{html.escape(record.verdict.title())}</span></div>'
    st.markdown(rows + "</div>", unsafe_allow_html=True)
