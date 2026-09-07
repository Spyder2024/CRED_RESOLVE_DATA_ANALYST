"""Render the S1 header and source-status pills."""

from datetime import date

import streamlit as st


def render(as_of: date, source: str) -> None:
    """Render the dashboard title, subtitle, and current data source."""
    source_class = source.lower()
    st.markdown(
        f"""<div class="dashboard-topbar"></div><div class="header-row"><div><div class="header-title">Collections Recovery — Fact Check</div><div class="header-subtitle">Independent audit of the +11% recovery claim · 12 months</div></div><div class="pill-row"><span class="status-pill">Data as-of: {as_of.strftime('%b %d, %Y').replace(' 0', ' ')}</span><span class="status-pill {source_class}">{source}</span></div></div>""",
        unsafe_allow_html=True,
    )
