"""Create the deterministic synthetic DuckDB views used when the golden database is absent."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).parents[2]
DEFAULT_DATABASE = ROOT / "data" / "golden.duckdb"


def _waterfall() -> pd.DataFrame:
    rows = [
        (1, "Reported improvement", 11.0, "start", "Legacy month-on-month definition"),
        (2, "- Duplicate payments", -1.4, "neg", "Same account, amount and payment event repeated"),
        (3, "- Denominator manipulation", -1.3, "neg", "Unsuccessful accounts were missing from the active population"),
        (4, "- Portfolio mix shift", -1.5, "neg", "Lower-risk and newer portfolios entered the denominator"),
        (5, "- Attribution bias", -1.2, "neg", "Payments were assigned to the latest interaction"),
        (6, "- Time and late data", -0.9, "neg", "Timezone and late-arriving events changed month placement"),
        (7, "- Vendor code changes", -1.3, "neg", "Disposition semantics changed across telephony vendors"),
        (8, "Verified improvement", 3.4, "end", "Fixed definitions and reconciled source events"),
    ]
    return pd.DataFrame(rows, columns=["component_order", "label", "value_pts", "component_type", "explanation"])


def _trend() -> pd.DataFrame:
    months = pd.date_range("2024-04-01", periods=12, freq="MS")
    reported = np.array([0.091, 0.093, 0.094, 0.096, 0.095, 0.097, 0.098, 0.099, 0.101, 0.102, 0.103, 0.10101])
    verified = np.array([0.091, 0.0918, 0.0925, 0.0933, 0.0928, 0.0936, 0.0941, 0.0950, 0.0960, 0.0969, 0.0975, 0.094094])
    return pd.DataFrame({
        "month": months.date,
        "reported_recovery_rate": reported,
        "verified_recovery_rate": verified,
        "verified_ci_low": verified - 0.004,
        "verified_ci_high": verified + 0.004,
        "is_structural_break": [False] * 6 + [True] + [False] * 5,
    })


def _truth() -> pd.DataFrame:
    rows = [
        ("Contact rate", 8.4, 2.1, "MISLEADING", "Denominator excludes accounts not attempted."),
        ("RPC", 6.8, 3.0, "MISLEADING", "Vendor disposition changes reclassified contacts."),
        ("PTP rate", 9.2, 5.6, "MISLEADING", "Latest-campaign attribution inflated exposure."),
        ("PTP kept", 4.5, 4.1, "GENUINE", "Kept promises remain stable after due-date matching."),
        ("Recovery rate", 11.0, 3.4, "MISLEADING", "Duplicate payments and denominator drift explain 7.6 pts."),
        ("Recovery/account", 8.7, 3.0, "MISLEADING", "Portfolio mix shifted toward smaller balances."),
        ("Recovery/agent-hour", 5.1, 2.8, "INCONCLUSIVE", "Session durations are incomplete in two vendors."),
        ("Cost per ₹", -6.2, -2.0, "INCONCLUSIVE", "Fully loaded channel cost is not consistently reported."),
        ("Channel conv.", 7.3, 2.6, "GENUINE", "Digital conversion improved in a matched holdout."),
    ]
    return pd.DataFrame(rows, columns=["metric_name", "reported_change", "verified_change", "verdict", "note"])


def _investment() -> pd.DataFrame:
    rows = [
        ("Better borrower targeting", 18.0, 10.0, 1.8, 2.3, 9, "MEDIUM", True, "Hold out 10% of eligible accounts and preserve fixed definitions.", 4.2),
        ("WhatsApp/digital engagement", 13.0, 10.0, 1.1, 1.6, 14, "MEDIUM", False, "Opt-in reach and message deliverability remain stable.", 2.8),
        ("AI voice automation", 11.0, 10.0, 0.8, 1.4, 16, "LOW", False, "Automation matches human RPC without complaint lift.", 3.1),
        ("Better telephony infrastructure", 8.0, 10.0, 0.6, 1.1, 20, "LOW", False, "Dropped-call reduction converts to incremental kept PTP.", 2.0),
        ("More collection agents", 9.0, 10.0, 0.7, 1.2, 18, "MEDIUM", False, "Hiring reaches productive hours without quality dilution.", 2.4),
        ("Field operations", 7.0, 10.0, 0.5, 1.0, 22, "LOW", False, "Visit productivity remains positive after travel cost.", 1.9),
    ]
    return pd.DataFrame(rows, columns=["option_name", "incremental_recovery_cr", "cost_cr", "roi_low", "roi_high", "breakeven_months", "confidence", "is_recommended", "key_assumption", "downside_cr"])


def generate_database(path: str | Path = DEFAULT_DATABASE, seed: int = 42) -> Path:
    """Write all contract views to a DuckDB file and return its path."""
    np.random.default_rng(seed)
    database_path = Path(path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists():
        database_path.unlink()
    connection = duckdb.connect(str(database_path))
    summary = pd.DataFrame([{
        "reported_change_pct": 11.0,
        "verified_change_pct": 3.4,
        "verified_ci_low": 2.5,
        "verified_ci_high": 4.3,
        "dq_issues_count": 6,
        "dq_adjustment_cr": 2.1,
        "data_asof_date": date(2025, 3, 31),
    }])
    counterfactual = pd.DataFrame([{"estimate_pts": -2.1, "ci_low": -3.0, "ci_high": -1.2, "method": "DiD + PSM, triangulated"}])
    tables = {"mart_kpi_summary": summary, "mart_waterfall": _waterfall(), "mart_monthly_trend": _trend(), "mart_metric_truth": _truth(), "mart_counterfactual": counterfactual, "mart_investment": _investment()}
    for name, frame in tables.items():
        connection.register(f"frame_{name}", frame)
        connection.execute(f"CREATE TABLE {name} AS SELECT * FROM frame_{name}")
        connection.execute(f"CREATE OR REPLACE VIEW {name}_view AS SELECT * FROM {name}")
    connection.close()
    database_path.with_suffix(".synthetic").write_text("Generated with seed 42\n", encoding="utf-8")
    return database_path


if __name__ == "__main__":
    print(generate_database())
