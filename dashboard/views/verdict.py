import streamlit as st

from dashboard.components.cards import (
    audit_timeline,
    evidence_card,
    executive_summary_banner,
    insight_card,
    kpi_card,
    section,
)
from dashboard.components.charts import trend_chart, waterfall_chart
from dashboard.components.shell import page_footer, page_shell
from dashboard.data import filter_trend


def render(data: dict) -> None:
    # -----------------------------------------------------------------
    # Phase 2: Enterprise Layout
    # 1. Top Nav & 2. Page Header
    # -----------------------------------------------------------------
    theme = page_shell(
        data=data,
        title="Executive Recovery Forensics",
        description="A forensic audit of Jan–Aug 2026 collections performance verifying headline recovery claims against DuckDB golden marts.",
        category="Overview",
        status_text="AUDITED",
        status_class="status-good",
    )

    # -----------------------------------------------------------------
    # 3. Executive Summary
    # -----------------------------------------------------------------
    executive_summary_banner(
        badge_text="VERDICT · CLAIM DOES NOT SURVIVE AUDIT",
        title="Reported +11.0% Recovery Claim Fails Independent Verification",
        body_text="The widely circulated +11.0% MoM recovery improvement cannot be reproduced under any standard definition. Audited recovery rate actually increased by +31.3% (95% CI: +20.4% to +43.1%). The legacy report severely understated true recovery due to unstandardized denominators and un-deduplicated transactions.",
        metrics=[
            ("Claimed Increase", "+11.0%"),
            ("Legacy Reconstruction", "+4.5%"),
            ("Audited Increase", "+31.3%"),
            ("Audit Gap", "+26.8 pts"),
        ],
        icon="!",
    )

    # -----------------------------------------------------------------
    # 4. KPI Cards
    # -----------------------------------------------------------------
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        kpi_card(
            label="CLAIMED METRIC",
            value="+11.0%",
            detail="Original unverified monthly report",
            badge="MISMATCH",
            badge_class="badge-red",
            icon="◌",
            trend="↓ Disproven",
        )
    with kpi_cols[1]:
        kpi_card(
            label="LEGACY RECONSTRUCTION",
            value="+4.5%",
            detail="Contacted-accounts baseline method",
            badge="BASELINE",
            badge_class="badge-amber",
            icon="≡",
            trend="Observed",
        )
    with kpi_cols[2]:
        kpi_card(
            label="AUDITED PERFORMANCE",
            value="+31.3%",
            detail="95% CI: +20.4% to +43.1%",
            badge="VERIFIED MART",
            badge_class="badge-teal",
            icon="✓",
            trend="↑ Verified",
        )
    with kpi_cols[3]:
        kpi_card(
            label="DEFINITION GAP",
            value="+26.8 pts",
            detail="Audited exceeds legacy baseline",
            badge="MATERIAL DRIFT",
            badge_class="badge-teal",
            icon="△",
            trend="+26.8 pts",
        )

    # -----------------------------------------------------------------
    # 5. Visualizations
    # -----------------------------------------------------------------
    section(
        title="Visualizations & Forensic Decompositions",
        description="Side-by-side reconciliation bridge and verified longitudinal trends with confidence intervals.",
    )

    viz_cols = st.columns([1.1, 1.3])
    with viz_cols[0]:
        st.markdown(
            "<div class='card-label' style='margin-bottom: 8px;'>DEFINITION BRIDGE: LEGACY TO AUDITED</div>",
            unsafe_allow_html=True,
        )
        waterfall_chart(data.get("waterfall"), theme)
    with viz_cols[1]:
        st.markdown(
            "<div class='card-label' style='margin-bottom: 8px;'>MONTHLY RECOVERY TRAJECTORY (JAN–AUG 2026)</div>",
            unsafe_allow_html=True,
        )
        complete_only = st.session_state.get("complete_only", True)
        filtered_trend = filter_trend(data.get("trend"), complete_only)
        trend_chart(filtered_trend, theme, complete_only)

    # -----------------------------------------------------------------
    # 6. Insights
    # -----------------------------------------------------------------
    section(
        title="Forensic Insights & Variance Drivers",
        description="Root causes for the 26.8 percentage-point gap between reporting layers.",
    )

    insight_cols = st.columns(3)
    with insight_cols[0]:
        insight_card(
            label="Denominator Shift",
            value="Eligible Cohorts vs Contacted",
            detail="Legacy metrics evaluated only successfully contacted accounts, inflating variance and missing uncontacted payers who settled via digital channels.",
        )
    with insight_cols[1]:
        insight_card(
            label="Transaction Deduplication",
            value="Duplicate Payment Reference Hash",
            detail="Reconciled multiple payment gateway callbacks into single golden transactions, preventing double-counting while preserving net settlement.",
        )
    with insight_cols[2]:
        insight_card(
            label="Longitudinal Consistency",
            value="Consistent Superiority Across Months",
            detail="Audited recovery rates exceeded legacy figures in all complete observation periods. The gap peaked in July 2026 before the provisional August cutoff.",
        )

    # -----------------------------------------------------------------
    # 7. Evidence
    # -----------------------------------------------------------------
    section(
        title="Evidence & Governance Matrix",
        description="Multi-pillar audit conclusions and institutional operational recommendations.",
    )

    evidence_cols = st.columns(4)
    with evidence_cols[0]:
        evidence_card(
            label="CLAIM VALIDITY",
            value="Claim Fails Audit",
            badge_text="NOT REPRODUCIBLE",
            badge_class="badge-red",
            detail="The +11.0% figure cannot be mathematically derived from the primary transaction and contact records.",
        )
    with evidence_cols[1]:
        evidence_card(
            label="TRUE RECOVERY",
            value="+31.3% Growth",
            badge_text="AUDITED",
            badge_class="badge-teal",
            detail="Actual performance exceeded legacy claims (+31.3% vs +4.5% baseline) due to organic multi-channel repayments.",
        )
    with evidence_cols[2]:
        evidence_card(
            label="STATISTICAL RIGOR",
            value="95% CI Interval",
            badge_text="ROBUST",
            badge_class="badge-teal",
            detail="Bootstrap bounds [+20.4%, +43.1%] strictly exclude both the legacy +4.5% baseline and claimed +11.0%.",
        )
    with evidence_cols[3]:
        evidence_card(
            label="CAPITAL DECISION",
            value="Pilot Only (Holdout)",
            badge_text="LOW CONFIDENCE",
            badge_class="badge-amber",
            detail="Targeting model lacks a randomized control group. ₹10 Cr deployment carries a modeled downside of ₹5.0 Cr.",
        )

    st.markdown("<div class='card-label' style='margin: 20px 0 8px;'>DECISION AUDIT TRAIL</div>", unsafe_allow_html=True)
    audit_timeline([
        ("Source Extraction", True),
        ("Schema Typing & Normalization", True),
        ("Entity Deduplication", True),
        ("Golden Marts Construction", True),
        ("Independent Audit", True),
        ("Leadership Publication", True),
    ])

    # -----------------------------------------------------------------
    # 8. Methodology
    # -----------------------------------------------------------------
    section(
        title="Methodology & Data Lineage",
        description="Strict semantic contracts and reproducible data transformations.",
    )

    st.markdown(
        """<div class='flow'>
            <div class='flow-step'>
                <b>1. Raw Extracts</b>
                <span class='muted'>17 CSV Source Tables</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>2. Staging & Cleaning</b>
                <span class='muted'>UTC Times, Deduplication</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>3. Golden Layer</b>
                <span class='muted'>Account-Day Grain</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>4. DuckDB Marts</b>
                <span class='muted'>7 Public Semantic Views</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>5. Analytics Platform</b>
                <span class='muted'>Forensic Presentation</span>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------
    # 9. Footer
    # -----------------------------------------------------------------
    page_footer(data)