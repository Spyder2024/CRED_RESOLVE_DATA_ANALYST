from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st


# Actual public mart columns discovered from data/golden.duckdb on 2026-09-09.
COLUMN_MAP = {
    "kpi": {
        "claimed": "reported_change_pct", "audited": "verified_change_pct",
        "ci_low": "verified_ci_low", "ci_high": "verified_ci_high",
        "dq_issues": "dq_issues_count", "dq_amount": "dq_adjustment_cr",
        "asof": "data_asof_date",
    },
    "trend": {
        "month": "month", "legacy": "reported_recovery_rate",
        "audited": "verified_recovery_rate", "ci_low": "verified_ci_low",
        "ci_high": "verified_ci_high", "break": "is_structural_break",
    },
    "legacy": {"month": "month", "rate": "reported_rate", "contacted": "contacted", "amount": "raw_amount"},
    "waterfall": {"order": "component_order", "label": "label", "value": "value_pts", "type": "component_type", "explanation": "explanation"},
    "truth": {"metric": "metric_name", "claimed": "reported_change", "audited": "verified_change", "verdict": "verdict", "note": "note"},
    "investment": {"option": "option_name", "incremental": "incremental_recovery_cr", "cost": "cost_cr", "roi_low": "roi_low", "roi_high": "roi_high", "months": "breakeven_months", "confidence": "confidence", "recommended": "is_recommended", "assumption": "key_assumption", "downside": "downside_cr"},
}

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "golden.duckdb"
MARTS = ["mart_kpi_summary", "mart_waterfall", "mart_monthly_trend", "mart_metric_truth", "mart_investment", "mart_legacy_monthly", "mart_counterfactual"]


def _synthetic() -> dict[str, Any]:
    rng = np.random.default_rng(42)
    months = pd.date_range("2026-01-01", "2026-08-01", freq="MS")
    legacy = np.array([0.118, 0.121, 0.127, 0.132, 0.138, 0.143, 0.163, 0.178])
    audited = np.array([0.142, 0.151, 0.165, 0.181, 0.202, 0.224, 0.248, 0.271])
    trend = pd.DataFrame({"month": months, "reported_recovery_rate": legacy, "verified_recovery_rate": audited, "verified_ci_low": audited - .012, "verified_ci_high": audited + .012, "is_structural_break": [False, False, False, False, False, False, True, False]})
    trend["is_partial"] = trend["month"].eq(pd.Timestamp("2026-08-01"))
    legacy_monthly = pd.DataFrame({"month": months, "contacted": rng.integers(800, 1200, 8), "raw_recovered": rng.integers(100, 200, 8), "raw_amount": rng.uniform(30, 50, 8), "reported_rate": legacy})
    waterfall = pd.DataFrame({"component_order": [1, 2, 3], "label": ["Legacy view", "Audit adjustments", "Audited view"], "value_pts": [4.5, 26.8, 31.3], "component_type": ["start", "increase", "end"], "explanation": ["Reported-style reconstruction", "Deduplication, denominator and reconciliation changes", "Audited recovery estimate"]})
    truth = pd.DataFrame({"metric_name": ["MoM recovery", "Recovery rate", "Collector productivity", "Channel conversion", "Cost per recovery", "Promise kept", "Roll-rate", "Cure rate", "Portfolio mix"], "reported_change": [0.110, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], "verified_change": [0.313, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], "verdict": ["REPRODUCIBLE", "MISLEADING", "INCONCLUSIVE", "INCONCLUSIVE", "INCONCLUSIVE", "INCONCLUSIVE", "INCONCLUSIVE", "INCONCLUSIVE", "INCONCLUSIVE"], "note": ["Audited definition differs from claim", "Legacy denominator", "Requires agent-hour table", "Requires channel outcome table", "Requires cost table", "Requires promise table", "Requires balance snapshots", "Requires cure definition", "Requires portfolio controls"]})
    investment = pd.DataFrame({"option_name": ["Better borrower targeting", "Agent coaching", "Channel mix", "Reminder cadence", "Settlement design", "Do nothing"], "incremental_recovery_cr": [0.18, 0.12, 0.09, 0.07, 0.11, 0.0], "cost_cr": [10.0, 2.5, 1.8, 1.2, 3.0, 0.0], "roi_low": [0.2, 0.3, 0.35, 0.4, 0.25, 0.0], "roi_high": [0.8, 1.1, 1.3, 1.5, 0.9, 0.0], "breakeven_months": [18, 14, 11, 9, 16, 0], "confidence": ["LOW", "LOW", "LOW", "LOW", "LOW", "N/A"], "is_recommended": [True, False, False, False, False, False], "key_assumption": ["5% lift — NOT established", "Training changes conversion", "Observed channel mix holds", "Response curve persists", "Offer acceptance persists", "No intervention"], "downside_cr": [5.0, 1.5, 0.8, 0.5, 1.8, 0.0]})
    kpi = pd.DataFrame([{ "reported_change_pct": 11.0, "verified_change_pct": 31.3, "verified_ci_low": 20.4, "verified_ci_high": 43.1, "dq_issues_count": 6, "dq_adjustment_cr": 17.2, "data_asof_date": pd.Timestamp("2026-08-08") }])
    dq = pd.DataFrame({"issue": ["Duplicate payment IDs", "Mixed status labels", "Timezone offsets", "Agent aliases", "Partial August", "Unmatched account IDs"], "severity": ["High", "Medium", "Medium", "Medium", "High", "Low"], "impact": ["Reconciled", "Reconciled", "Review", "Review", "Provisional", "Review"], "detail": ["Payment rows deduplicated", "Status values standardized", "Events normalized to UTC", "Identity map incomplete", "Ends Aug 8", "Entity resolution residual"]})
    return {"source": "SYNTHETIC", "kpi": kpi, "trend": trend, "legacy": legacy_monthly, "waterfall": waterfall, "truth": truth, "investment": investment, "dq": dq, "counterfactual": pd.DataFrame([{ "estimate_pts": np.nan, "ci_low": np.nan, "ci_high": np.nan, "method": "NOT IDENTIFIABLE — no holdout" }])}


def _read_mart(con: Any, name: str) -> pd.DataFrame:
    try:
        return con.execute(f"SELECT * FROM {name}").fetchdf()
    except Exception:
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_data(theme: str = "light", filter_signature: str = "default") -> dict[str, Any]:
    del theme, filter_signature
    if not DB_PATH.exists():
        source_dir = ROOT / "data" / "collections_30k_dataset (4)"
        if source_dir.exists():
            try:
                from src.pipeline import build_golden
                build_golden()
            except Exception:
                pass
    if not DB_PATH.exists():
        return _synthetic()
    try:
        import duckdb
        con = duckdb.connect(str(DB_PATH), read_only=True)
        key_names = {"mart_kpi_summary": "kpi", "mart_monthly_trend": "trend", "mart_legacy_monthly": "legacy", "mart_metric_truth": "truth", "mart_investment": "investment", "mart_waterfall": "waterfall", "mart_counterfactual": "counterfactual"}
        frames = {key_names[name]: _read_mart(con, name) for name in MARTS}
        con.close()
        if not frames.get("kpi", pd.DataFrame()).empty:
            trend = frames.get("monthly_trend", pd.DataFrame())
            if not trend.empty:
                trend["is_partial"] = pd.to_datetime(trend[COLUMN_MAP["trend"]["month"]]).dt.month.eq(8)
            dq = pd.DataFrame({"issue": ["Duplicate and conflicting records", "Status normalization", "Timezone normalization", "Agent aliases", "Partial August", "Entity resolution"], "severity": ["High", "Medium", "Medium", "Medium", "High", "Low"], "impact": ["Reconciled"] * 6, "detail": ["See quality_checks", "Aliases standardized", "UTC review required", "Mapping remains incomplete", "Ends Aug 8", "Residual unmatched IDs"]})
            frames["dq"] = dq
            return {"source": "GOLDEN", **frames}
    except Exception:
        pass
    return _synthetic()


def value(frame: pd.DataFrame, key: str, group: str, default: Any = None) -> Any:
    column = COLUMN_MAP[group].get(key, key)
    if frame.empty or column not in frame.columns:
        return default
    return frame.iloc[0][column]


def filter_trend(frame: pd.DataFrame, complete_only: bool) -> pd.DataFrame:
    if frame.empty:
        return frame
    result = frame.copy()
    month = COLUMN_MAP["trend"]["month"]
    result[month] = pd.to_datetime(result[month])
    if "is_partial" not in result.columns:
        result["is_partial"] = result[month].dt.month.eq(8)
    if complete_only:
        result = result[~result["is_partial"]]
    return result
