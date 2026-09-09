import pandas as pd
import streamlit as st

from dashboard.components.cards import insight_card, kpi_card, section
from dashboard.components.shell import page_footer, page_shell


def render(data: dict) -> None:
    page_shell(
        data=data,
        title="Methodology & Data Lineage",
        description="Formal semantic contracts, architectural data flows, and end-to-end reproducible execution pipelines.",
        category="Verdict",
        status_text="DETERMINISTIC",
        status_class="status-good",
    )

    section("Production Pipeline Architecture", "Deterministic DAG producing immutable golden marts from raw collections data.")
    st.markdown(
        """<div class='flow'>
            <div class='flow-step'>
                <b>1. Raw Ingestion</b>
                <span class='muted'>17 CSV Tables · 30k+ Events</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>2. Staging Layer</b>
                <span class='muted'>Schema Typing & UTC Normalization</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>3. Entity Resolution</b>
                <span class='muted'>Deduplication & Hash Matching</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>4. Golden Marts</b>
                <span class='muted'>7 Public DuckDB Analytical Views</span>
            </div>
            <div style='color:var(--secondary);'>→</div>
            <div class='flow-step'>
                <b>5. Executive Platform</b>
                <span class='muted'>Read-Only Forensics UI</span>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    section("Core Architectural Metrics", "Pipeline throughput and validation statistics.")
    cols = st.columns(4)
    with cols[0]:
        kpi_card("SOURCE TABLES", "17 Tables", "Standardized CSV extracts", "INPUTS", "badge-teal", "📁")
    with cols[1]:
        kpi_card("PRIMARY GRAIN", "Account-Day", "Cleaned atomic fact level", "GOLDEN", "badge-teal", "✨")
    with cols[2]:
        kpi_card("ANALYTICAL MARTS", "7 Views", "Exposed via golden.duckdb", "PUBLIC", "badge-teal", "📊")
    with cols[3]:
        kpi_card("REPRODUCIBILITY", "100% Deterministic", "Seed: 42 / Exact SQL DAG", "AUDITED", "badge-teal", "🔒")

    section("Semantic Metric Contracts", "Formal mathematical definitions enforced across all reporting queries.")
    contracts = pd.DataFrame([
        {
            "Metric": "Audited Recovery Rate",
            "Mathematical Definition": "Distinct accounts with settled payments in 30-day window / Total assigned eligible accounts at month start",
            "Baseline Denominator": "All Assigned Eligible Accounts",
            "Audit Status": "Verified",
        },
        {
            "Metric": "Legacy Recovery Rate",
            "Mathematical Definition": "Distinct accounts with settled payments / Total successfully contacted accounts in month",
            "Baseline Denominator": "Contacted Accounts Only (Biased)",
            "Audit Status": "Rejected (Misleading)",
        },
        {
            "Metric": "Definition Gap",
            "Mathematical Definition": "Audited Recovery Rate (%) − Legacy Recovery Rate (%)",
            "Baseline Denominator": "Percentage Points (pts)",
            "Audit Status": "Verified (+26.8 pts)",
        },
        {
            "Metric": "Cost per Rupee Recovered",
            "Mathematical Definition": "Fully loaded operational costs (telephony, agent hours, messaging) / Total settled recovery amount",
            "Baseline Denominator": "Settled Monetary Volume",
            "Audit Status": "Inconclusive (Awaiting Data)",
        },
        {
            "Metric": "PTP Keep Rate",
            "Mathematical Definition": "Distinct PTP promises settled on or before due date / Total valid PTPs registered in window",
            "Baseline Denominator": "All Valid PTP Promises",
            "Audit Status": "Inconclusive (Awaiting Data)",
        },
    ])
    st.dataframe(contracts, hide_index=True, width="stretch")

    section("Reproducibility & Verification Guide", "Execute the entire analytical DAG from source to dashboard.")
    st.code(
        """# 1. Activate isolated Python virtual environment
.\\.venv\\Scripts\\Activate.ps1

# 2. Re-run deterministic cleaning, entity resolution, and DuckDB mart publication
python -m src.pipeline

# 3. Launch the enterprise forensics dashboard
streamlit run dashboard\\app.py""",
        language="powershell",
    )

    page_footer(data)