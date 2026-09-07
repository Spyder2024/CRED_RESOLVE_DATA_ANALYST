"""Render the S3 waterfall showing the gap between reported and verified change."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import PLOTLY_TEMPLATE, TOKENS


def render(waterfall: pd.DataFrame, reported: float, verified: float) -> None:
    """Render an assertion-led waterfall with explanatory hover text."""
    figure = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute"] + ["relative"] * (len(waterfall) - 2) + ["total"],
        x=waterfall["label"].tolist(),
        y=waterfall["value_pts"].tolist(),
        text=[f"{value:+.1f} pts" for value in waterfall["value_pts"]],
        textposition="outside",
        connector={"line": {"color": TOKENS["card_border"], "width": 1}},
        increasing={"marker": {"color": TOKENS["genuine_teal"]}},
        decreasing={"marker": {"color": TOKENS["misleading_red"]}},
        totals={"marker": {"color": TOKENS["primary_navy"]}},
        customdata=waterfall[["explanation"]],
        hovertemplate="<b>%{x}</b><br>%{y:+.1f} pts<br>%{customdata[0]}<extra></extra>",
    ))
    figure.update_layout(template=PLOTLY_TEMPLATE, title=f"{reported - verified:.1f} pts of the +{reported:.1f}% gain is an artifact", yaxis_title="Percentage points", showlegend=False, height=330)
    st.plotly_chart(figure, width="stretch", config={"displayModeBar": False})
    st.caption("Residual within ±0.3 pts · full lineage: sql/04_metrics/")
