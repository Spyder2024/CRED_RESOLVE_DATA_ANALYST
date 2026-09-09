import streamlit as st

from dashboard.components.cards import insight_card, kpi_card, section
from dashboard.components.charts import trend_chart, waterfall_chart
from dashboard.components.shell import page_footer, page_shell
from dashboard.components.tables import monthly_table
from dashboard.data import filter_trend


def render(data: dict) -> None:
    theme = page_shell(
        data=data,
        title="Recovery Forensics & Trends",
        description="Granular comparison of audited eligible-account recovery rates against legacy contacted-account metrics across all observation windows.",
        category="Overview",
        status_text="AUDITED",
        status_class="status-good",
    )

    trend_raw = data.get("trend")
    complete_only = st.session_state.get("complete_only", True)
    trend = filter_trend(trend_raw, complete_only)

    # Top summary cards
    cols = st.columns(4)
    with cols[0]:
        kpi_card("AUDITED PEAK", "27.1%", "Observed in August 2026", "PEAK", "badge-teal", "↑")
    with cols[1]:
        kpi_card("LEGACY PEAK", "17.8%", "Observed in August 2026", "BASELINE", "badge-amber", "≡")
    with cols[2]:
        kpi_card("MAX SPREAD", "+9.3 pts", "July 2026 complete month", "WIDE", "badge-teal", "△")
    with cols[3]:
        status_badge = "EXCLUDED" if complete_only else "INCLUDED"
        kpi_card("AUG PARTIAL", "Aug 8 Cutoff", "Trailing 8 days of data", status_badge, "badge-amber", "⏱")

    section("Longitudinal Trend Analysis", "Legacy view remains dashed grey; audited is solid teal with 95% confidence interval.")
    trend_chart(trend, theme, complete_only)

    section("Bridge Decomposition", "Detailed breakdown of audit adjustments between legacy reconstruction (+4.5%) and audited result (+31.3%).")
    viz_cols = st.columns([1.5, 1])
    with viz_cols[0]:
        waterfall_chart(data.get("waterfall"), theme)
    with viz_cols[1]:
        insight_card(
            label="Attribution Choice",
            value="Why Audited Rates Are Higher",
            detail="By auditing the total eligible portfolio rather than solely agent-contacted accounts, collections through autonomous digital rails (app notifications, automated UPI intents) are properly attributed to portfolio performance rather than dropped.",
        )

    section("Monthly Reconciliation Ledger", "Source mart breakdown with sign-colored indicators and explicit partial-month flags.")
    monthly_table(filter_trend(trend_raw, False))

    page_footer(data)