"""Cached DuckDB data access with a contract-identical synthetic fallback."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

from src.synth.generate_dashboard_data import DEFAULT_DATABASE, generate_database

REQUIRED_COLUMNS = {
    "mart_kpi_summary": {"reported_change_pct", "verified_change_pct", "verified_ci_low", "verified_ci_high", "dq_issues_count", "dq_adjustment_cr", "data_asof_date"},
    "mart_waterfall": {"component_order", "label", "value_pts", "component_type", "explanation"},
    "mart_monthly_trend": {"month", "reported_recovery_rate", "verified_recovery_rate", "verified_ci_low", "verified_ci_high", "is_structural_break"},
    "mart_metric_truth": {"metric_name", "reported_change", "verified_change", "verdict", "note"},
    "mart_counterfactual": {"estimate_pts", "ci_low", "ci_high", "method"},
    "mart_investment": {"option_name", "incremental_recovery_cr", "cost_cr", "roi_low", "roi_high", "breakeven_months", "confidence", "is_recommended", "key_assumption", "downside_cr"},
}


def _query_contract(database_path: Path) -> dict[str, pd.DataFrame]:
    connection = duckdb.connect(str(database_path), read_only=True)
    frames: dict[str, pd.DataFrame] = {}
    try:
        for view_name, required in REQUIRED_COLUMNS.items():
            frame = connection.execute(f"SELECT * FROM {view_name}").df()
            missing = required.difference(frame.columns)
            if missing:
                raise ValueError(f"{view_name} is missing columns: {', '.join(sorted(missing))}")
            frames[view_name] = frame
    finally:
        connection.close()
    return frames


@st.cache_data(ttl=3600, show_spinner=False)
def load_golden(database_path: str = str(DEFAULT_DATABASE), database_mtime: float = 0) -> tuple[dict[str, pd.DataFrame], str]:
    """Load every mart view from golden.duckdb, generating synthetic data only when absent."""
    path = Path(database_path)
    source = "GOLDEN"
    if not path.exists():
        generate_database(path, seed=42)
        source = "SYNTHETIC"
    elif path.with_suffix(".synthetic").exists() and path.with_suffix(".synthetic").stat().st_mtime >= path.stat().st_mtime:
        source = "SYNTHETIC"
    frames = _query_contract(path)
    frames["mart_monthly_trend"]["month"] = pd.to_datetime(frames["mart_monthly_trend"]["month"])
    frames["mart_kpi_summary"]["data_asof_date"] = pd.to_datetime(frames["mart_kpi_summary"]["data_asof_date"])
    return frames, source


def load_dashboard_data() -> tuple[dict[str, pd.DataFrame], str]:
    """Resolve the current database path and cache key for a fast warm reload."""
    path = DEFAULT_DATABASE
    marker = path.with_suffix(".synthetic")
    mtime = max(path.stat().st_mtime if path.exists() else 0, marker.stat().st_mtime if marker.exists() else 0)
    return load_golden(str(path), mtime)
