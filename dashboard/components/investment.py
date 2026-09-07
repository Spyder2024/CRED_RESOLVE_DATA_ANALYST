"""Render the S6 ₹10 Cr recommendation and comparison expander."""

import html

import pandas as pd
import streamlit as st


def _cr(value: float) -> str:
    return f"₹{value:.1f} Cr"


def render(investment: pd.DataFrame) -> None:
    """Render the recommended investment and all six modeled options."""
    recommendation = investment.loc[investment["is_recommended"]].iloc[0]
    st.markdown('<div class="section-label">Recommendation · ₹10 Cr deployment</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f'<div class="investment-name">{html.escape(recommendation.option_name)}</div><div class="investment-rationale">Highest modeled incremental recovery with a measurable holdout path.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mini-grid"><div><div class="mini-label">Expected ROI</div><div class="mini-value">×{recommendation.roi_low:.1f}–{recommendation.roi_high:.1f}</div></div><div><div class="mini-label">Break-even</div><div class="mini-value">~{int(recommendation.breakeven_months)} months</div></div><div><div class="mini-label">Downside at risk</div><div class="mini-value">{_cr(recommendation.downside_cr)}</div></div><div><div class="mini-label">Confidence</div><div class="mini-value">{recommendation.confidence}</div></div></div><div class="assumption"><b>Key assumption:</b> {html.escape(recommendation.key_assumption)}</div>', unsafe_allow_html=True)
    with st.expander("Compare all six options"):
        display = investment.copy()
        display["Incremental recovery"] = display["incremental_recovery_cr"].map(_cr)
        display["Cost"] = display["cost_cr"].map(_cr)
        display["ROI range"] = display.apply(lambda row: f"×{row.roi_low:.1f}–{row.roi_high:.1f}", axis=1)
        display["Break-even"] = display["breakeven_months"].map(lambda value: f"{int(value)} mo")
        display["Downside"] = display["downside_cr"].map(_cr)
        display["Option"] = display["option_name"]
        display["Confidence"] = display["confidence"]
        st.dataframe(display[["Option", "Incremental recovery", "Cost", "ROI range", "Break-even", "Downside", "Confidence"]], width="stretch", hide_index=True, column_config={"Option": st.column_config.TextColumn("Option"), "Incremental recovery": st.column_config.TextColumn("Incremental recovery"), "Cost": st.column_config.TextColumn("Cost")})
