import pandas as pd
import streamlit as st


def monthly_table(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.info("No monthly records available for the selected filter.")
        return
    view = frame.copy()
    view["Month"] = pd.to_datetime(view["month"]).dt.strftime("%b %Y")
    view["Legacy Rate"] = (view["reported_recovery_rate"] * 100).round(1).astype(str) + "%"
    view["Audited Rate"] = (view["verified_recovery_rate"] * 100).round(1).astype(str) + "%"
    view["95% CI Lower"] = (view["verified_ci_low"] * 100).round(1).astype(str) + "%"
    view["95% CI Upper"] = (view["verified_ci_high"] * 100).round(1).astype(str) + "%"
    view["Status"] = view["is_partial"].map({True: "Provisional (Aug 8)", False: "Complete"})

    st.dataframe(
        view[["Month", "Legacy Rate", "Audited Rate", "95% CI Lower", "95% CI Upper", "Status"]],
        hide_index=True,
        width="stretch",
    )


def truth_table(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.info("No metric truth table entries available.")
        return
    view = frame.rename(
        columns={
            "metric_name": "Operating Metric",
            "verdict": "Audit Verdict",
            "note": "Root Cause / Unlock Requirement",
        }
    )
    st.dataframe(
        view[["Operating Metric", "Audit Verdict", "Root Cause / Unlock Requirement"]],
        hide_index=True,
        width="stretch",
    )
