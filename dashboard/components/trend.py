"""Render the S4 audited-versus-legacy monthly trend."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import PLOTLY_TEMPLATE, TOKENS


def render(trend: pd.DataFrame, reported: float, verified: float) -> None:
    """Render the twelve-month trend with confidence band and structural break."""
    latest_gap = reported - verified
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=trend["month"], y=trend["verified_ci_high"] * 100, mode="lines", line={"width": 0}, showlegend=False, hoverinfo="skip"))
    figure.add_trace(go.Scatter(x=trend["month"], y=trend["verified_ci_low"] * 100, mode="lines", line={"width": 0}, fill="tonexty", fillcolor="rgba(26,54,93,0.12)", name="95% CI", hoverinfo="skip"))
    figure.add_trace(go.Scatter(x=trend["month"], y=trend["reported_recovery_rate"] * 100, mode="lines+markers", name="Reported (legacy)", line={"color": TOKENS["legacy_grey"], "dash": "dash", "width": 2}, marker={"size": 5}))
    figure.add_trace(go.Scatter(x=trend["month"], y=trend["verified_recovery_rate"] * 100, mode="lines+markers", name="Verified (audited)", line={"color": TOKENS["primary_navy"], "width": 2.5}, marker={"size": 5}))
    breaks = trend.loc[trend["is_structural_break"]]
    for month in breaks["month"]:
        figure.add_vline(x=month, line_color=TOKENS["inconclusive_amber"], line_dash="dash", line_width=1)
        figure.add_annotation(x=month, y=float(trend[["reported_recovery_rate", "verified_recovery_rate"]].max().max() * 100), text="Targeting change", showarrow=False, yshift=12, font={"color": TOKENS["inconclusive_amber"], "size": 10})
    figure.update_layout(template=PLOTLY_TEMPLATE, title=f"The legacy view ends {latest_gap:.1f} pts above verified recovery", yaxis_title="Recovery rate (%)", yaxis_ticksuffix="%", height=320, hovermode="x unified")
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
