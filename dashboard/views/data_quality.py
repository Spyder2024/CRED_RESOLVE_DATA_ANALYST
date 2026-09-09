import streamlit as st

from dashboard.components.cards import insight_card, kpi_card, section
from dashboard.components.shell import page_footer, page_shell


def render(data: dict) -> None:
    page_shell(
        data=data,
        title="Data Quality & Integrity",
        description="Comprehensive audit of data cleaning, deduplication rules, schema normalization, and the ₹17.2 Cr reconciliation.",
        category="Overview",
        status_text="VERIFIED",
        status_class="status-good",
    )

    section("Pipeline Data Funnel", "Transformation of heterogeneous raw exports into standardized golden marts.")
    funnel_cols = st.columns(4)
    with funnel_cols[0]:
        kpi_card("RAW EXTRACTS", "17 Tables", "Source CSVs from collection systems", "UNAUDITED", "badge-amber", "📂")
    with funnel_cols[1]:
        kpi_card("GOLDEN GRAIN", "Account-Day", "Deduplicated entity records", "CLEANED", "badge-teal", "✨")
    with funnel_cols[2]:
        kpi_card("PUBLIC MARTS", "7 Views", "Semantic contracts for reporting", "STANDARDIZED", "badge-teal", "📊")
    with funnel_cols[3]:
        kpi_card("RECONCILIATION", "₹17.2 Cr", "Deduplicated & normalized volume", "ADJUSTMENT", "badge-teal", "⚖")

    section("Reconciliation Accounting Note", "Crucial context on the headline ₹17.2 Cr figure.")
    st.markdown(
        """<div class='callout' style='border-left: 4px solid var(--teal);'>
            <div style='display:flex;align-items:center;gap:10px;'>
                <span class='badge-teal'>ACCOUNTING CLARIFICATION</span>
                <b style='font-size:15px;'>₹17.2 Cr is a Data Reconciliation Adjustment — Not Lost Recovery</b>
            </div>
            <p class='muted' style='margin-top:6px;font-size:13px;line-height:1.6;'>
                This amount represents payments reconciled due to duplicate webhook retries, multi-timezone cross-midnight posts, and misaligned account identifiers. No funds were misplaced or leaked; this is an analytical normalization required to build sound golden marts.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    section("Tracked Data Quality Register", "Six material data quality issues identified and systematically remediated.")
    dq = data.get("dq")
    if dq is not None and not dq.empty:
        selected = st.dataframe(
            dq,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            width="stretch",
            key="dq_table",
        )
        if selected.selection.rows:
            row = dq.iloc[selected.selection.rows[0]]
            st.info(f"Selected Issue: **{row['issue']}** — {row['detail']} (Severity: {row['severity']}, Status: {row['impact']})")

    section("Systemic Operational Considerations", "Key observations affecting multi-channel behavioral modeling.")
    obs_cols = st.columns(3)
    with obs_cols[0]:
        insight_card(
            label="Timezone Harmonization",
            value="UTC Standardization",
            detail="Raw logs mixed IST, UTC, and legacy server timestamps. All events have been normalized to UTC; cross-midnight cutoffs have been resolved.",
        )
    with obs_cols[1]:
        insight_card(
            label="Agent Alias Resolution",
            value="Incomplete Identity Mapping",
            detail="Collector agent IDs are inconsistently mapped across dialer vs CRM tables. Productivity claims remain statistically inconclusive.",
        )
    with obs_cols[2]:
        insight_card(
            label="Provisional Close",
            value="August 8 Cut-off",
            detail="The dataset concludes on August 8, 2026. August is classified as provisional and excluded from headline growth calculations.",
        )

    page_footer(data)