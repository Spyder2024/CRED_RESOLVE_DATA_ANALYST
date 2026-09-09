import streamlit as st

from dashboard.components.cards import (
    executive_summary_banner,
    insight_card,
    kpi_card,
    section,
)
from dashboard.components.shell import page_footer, page_shell


def render(data: dict) -> None:
    page_shell(
        data=data,
        title="₹10 Cr Capital Allocation",
        description="Economic audit, downside risk modeling, and sensitivity analysis for the proposed ₹10 Cr borrower targeting initiative.",
        category="Verdict",
        status_text="PILOT ONLY",
        status_class="status-warn",
    )

    executive_summary_banner(
        badge_text="CAPITAL ADVISORY · HIGH DOWNSIDE RISK",
        title="Borrower Targeting: Recommend Phased Pilot, Not Full Rollout",
        body_text="Allocating ₹10 Cr to full-scale model rollout without a randomized holdout carries up to ₹5.0 Cr in unhedged downside. The proposed 5% recovery lift is an observational correlation, not an established causal relationship.",
        metrics=[
            ("Proposed Capital", "₹10.0 Cr"),
            ("Expected Recovery", "₹0.18 Cr"),
            ("Modeled ROI Range", "0.2× – 0.8×"),
            ("Maximum Downside", "₹5.0 Cr"),
        ],
        icon="⚠️",
    )

    section("Capital & Payback Profile", "Core financial projections under base-case operational assumptions.")
    cols = st.columns(6)
    with cols[0]:
        kpi_card("INVESTMENT", "₹10.0 Cr", "Proposed capital outlay", "CAPEX", "badge-amber", "💰")
    with cols[1]:
        kpi_card("EXPECTED LIFT", "₹0.18 Cr", "Assumed 5% recovery lift", "PROJECTED", "badge-amber", "📈")
    with cols[2]:
        kpi_card("ROI MULTIPLE", "0.2× – 0.8×", "Unfavorable expected return", "SUB-PAR", "badge-red", "⚖")
    with cols[3]:
        kpi_card("BREAKEVEN", "18 Months", "Long operational horizon", "DELAYED", "badge-amber", "⏳")
    with cols[4]:
        kpi_card("DOWNSIDE", "₹5.0 Cr", "Unhedged financial risk", "HIGH RISK", "badge-red", "🛡")
    with cols[5]:
        kpi_card("CONFIDENCE", "LOW", "No randomized baseline", "CAUTION", "badge-red", "🔍")

    section("Live Sensitivity Simulator", "Interactive stress-test evaluating returns across varied incremental lift scenarios.")
    lift = st.slider(
        "Assumed Incremental Recovery Lift (%)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        format="%.1f%%",
        help="Adjust the theoretical recovery lift above baseline to observe modeled impact.",
    )
    recovery = 10.0 * (lift / 5.0) * 0.18 if lift > 0 else 0.0
    roi = recovery / 10.0
    breakeven = (10.0 / recovery * 18.0) if recovery > 0 else float("inf")

    sim_cols = st.columns(3)
    with sim_cols[0]:
        kpi_card("MODELED RECOVERY", f"₹{recovery:.2f} Cr", f"At {lift:.1f}% assumed lift", "SIMULATED", "badge-teal", "₹")
    with sim_cols[1]:
        kpi_card("MODELED ROI", f"{roi:.2f}×", "Net capital return ratio", "SIMULATED", "badge-teal" if roi >= 1.0 else "badge-red", "×")
    with sim_cols[2]:
        be_str = "Not Reached" if recovery == 0 else f"{breakeven:.0f} Months"
        kpi_card("BREAKEVEN TIME", be_str, "Capital recovery timeline", "SIMULATED", "badge-amber", "⏱")

    section("Counterfactual & Identifiability", "Why observational data cannot justify full capital commitment.")
    crit_cols = st.columns(2)
    with crit_cols[0]:
        insight_card(
            label="Missing Counterfactual",
            value="No Untreated Holdout Group",
            detail="The historical dataset lacks an A/B control group. High-score borrowers who paid might have paid regardless of targeting, confounding organic intent with intervention impact.",
        )
    with crit_cols[1]:
        insight_card(
            label="Statistical Identifiability",
            value="Selection Bias in Outreach",
            detail="Collectors cherry-picked high-propensity accounts, artificially inflating contacted recovery rates. Causal attribution requires a pre-registered randomized holdout.",
        )

    section("Recommended Phased Experimentation Plan", "Pre-conditions required prior to authorizing full ₹10 Cr deployment.")
    steps = [
        ("1. Cohort Specification", "Define eligible DPD 30–90 borrower universe with standardized risk scoring."),
        ("2. Randomization", "Isolate a strict 10% un-contacted holdout cohort via deterministic cryptographic hashing."),
        ("3. Pre-Registration", "Pre-register primary outcome metrics (settled recovery, contact fatigue, complaint rates)."),
        ("4. Granular Tracking", "Capture channel delivery logs, operational costs, and agent-hour allocations."),
        ("5. Two-Cycle Trial", "Execute across 60 days to span two complete monthly settlement cycles."),
        ("6. Go/No-Go Review", "Scale exclusively if lower bound of treatment lift confidence interval exceeds hurdle ROI (1.5×)."),
    ]
    for num_title, desc in steps:
        st.markdown(
            f"""<div style='display:flex;align-items:flex-start;gap:12px;padding:8px 0;'>
                <span class='badge-teal' style='flex-shrink:0;'>{num_title[:2]}</span>
                <div>
                    <b>{num_title[3:]}</b>: <span class='muted'>{desc}</span>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    page_footer(data)