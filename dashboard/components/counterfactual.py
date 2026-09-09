"""Render the S5 targeting counterfactual callout."""

import pandas as pd
import streamlit as st


def render(counterfactual: pd.Series) -> None:
    """Render the triangulated counterfactual in one decision sentence."""
    if pd.isna(counterfactual["estimate_pts"]):
        st.markdown(f'<div class="callout">Counterfactual not identified from the supplied extract: no untreated targeting holdout is available · {counterfactual["method"]}.</div>', unsafe_allow_html=True)
        return
    estimate = float(counterfactual["estimate_pts"])
    low = float(counterfactual["ci_low"])
    high = float(counterfactual["ci_high"])
    st.markdown(f'<div class="callout">If targeting had not changed: verified recovery would be {estimate:+.1f} pts lower today (95% CI {low:+.1f} to {high:+.1f}) · {counterfactual["method"]}.</div>', unsafe_allow_html=True)
