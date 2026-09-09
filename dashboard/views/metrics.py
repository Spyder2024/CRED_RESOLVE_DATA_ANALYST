import streamlit as st

from dashboard.components.cards import (
    empty_state,
    executive_summary_banner,
    insight_card,
    kpi_card,
    section,
)
from dashboard.components.shell import page_footer, page_shell


def render(data: dict) -> None:
    page_shell(
        data=data,
        title="Metrics & Confidence Truth Table",
        description="Comprehensive audit of 9 core operational metrics, categorizing each by evidentiary validity and data availability.",
        category="Verdict",
        status_text="8 OF 9 UNVERIFIED",
        status_class="status-warn",
    )

    executive_summary_banner(
        badge_text="AUDIT GOVERNANCE · METRIC INTEGRITY",
        title="Only 1 of 9 Operating Metrics Survives Independent Audit",
        body_text="Longitudinal recovery change is REPRODUCIBLE under verified definitions (+31.3%). The legacy recovery rate is classified as MISLEADING due to selective cohort denominators. The remaining 7 metrics cannot be validated without missing operational tables.",
        metrics=[
            ("Reproducible", "1 Metric"),
            ("Misleading", "1 Metric"),
            ("Inconclusive", "7 Metrics"),
            ("Governance Rating", "High Strictness"),
        ],
        icon="⚖",
    )

    section("Metric Classification Summary", "Audited status across all operational domains.")
    cols = st.columns(3)
    with cols[0]:
        kpi_card("REPRODUCIBLE", "1 Metric", "MoM audited recovery growth (+31.3%)", "VERIFIED", "badge-teal", "✓")
    with cols[1]:
        kpi_card("MISLEADING", "1 Metric", "Legacy contacted-account recovery rate", "REJECTED", "badge-red", "✗")
    with cols[2]:
        kpi_card("INCONCLUSIVE", "7 Metrics", "Agent hours, channel costs, promise kept", "UNMAPPED", "badge-amber", "⏳")

    section("Interactive Metric Truth Register", "Click any row in the register to view root-cause analysis and data unlock requirements.")
    truth = data.get("truth")
    if truth is not None and not truth.empty:
        truth_view = truth.rename(
            columns={
                "metric_name": "Operating Metric",
                "verdict": "Audit Classification",
                "note": "Root Cause / Data Dependency",
            }
        )
        selected = st.dataframe(
            truth_view[["Operating Metric", "Audit Classification", "Root Cause / Data Dependency"]],
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            width="stretch",
            key="truth_table_select",
        )
        if selected.selection.rows:
            row = truth.iloc[selected.selection.rows[0]]
            status_badge = (
                "badge-teal" if row["verdict"] == "REPRODUCIBLE"
                else "badge-red" if row["verdict"] == "MISLEADING"
                else "badge-amber"
            )
            st.markdown(
                f"""<div class='callout' style='margin-top: 14px;'>
                    <div style='display:flex;align-items:center;gap:10px;'>
                        <span class='{status_badge}'>{row['verdict']}</span>
                        <b style='font-size:16px;'>{row['metric_name']}</b>
                    </div>
                    <div class='muted' style='margin-top:6px;'>
                        <b>Diagnostic:</b> {row['note']}
                    </div>
                    <div style='margin-top:8px;'>
                        <span class='badge-amber'>Data Unlock Path</span>
                        <span style='font-size:13px; margin-left:8px;'>Requires publishing primary operational telemetry and binding foreign keys.</span>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
    else:
        empty_state(
            title="Metric Mart Unavailable",
            reason="The mart_metric_truth view is not currently materialized.",
            unlock="Run python -m src.pipeline to generate golden marts.",
        )

    section("Operational Dependencies", "Data telemetry required to unlock full operational analytics.")
    dep_cols = st.columns(3)
    with dep_cols[0]:
        insight_card(
            label="Agent Telemetry",
            value="Logged-In Productive Hours",
            detail="To evaluate true collector productivity, agent active dialer time must be captured rather than inferred from disposition count.",
        )
    with dep_cols[1]:
        insight_card(
            label="Cost Accounting",
            value="Channel Delivery Invoices",
            detail="Computing cost per rupee recovered requires binding vendor SMS/IVR rates and telephony egress charges to recipient accounts.",
        )
    with dep_cols[2]:
        insight_card(
            label="Cohort Aging",
            value="Daily Balance Snapshots",
            detail="Roll-rate and cure-rate computations require daily ledger balances at fixed intervals, not merely payment event streams.",
        )

    page_footer(data)