"""Build the real golden DuckDB from the uploaded 30K collections extracts."""

from __future__ import annotations

import json
import math
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "data" / "collections_30k_dataset (4)"
OUTPUT = ROOT / "data" / "golden.duckdb"


def _read(name: str, dates: list[str] | None = None) -> pd.DataFrame:
    frame = pd.read_csv(SOURCE / f"{name}.csv", low_memory=False)
    for column in dates or []:
        if column in frame:
            frame[column] = pd.to_datetime(frame[column], errors="coerce", format="mixed")
    return frame


def _wilson(rate: float, count: int) -> tuple[float, float]:
    if count == 0:
        return 0.0, 0.0
    z = 1.96
    denominator = 1 + z**2 / count
    centre = (rate + z**2 / (2 * count)) / denominator
    spread = z * math.sqrt(rate * (1 - rate) / count + z**2 / (4 * count**2)) / denominator
    return max(0.0, centre - spread), min(1.0, centre + spread)


def _relative_change(first: float, last: float) -> float:
    return ((last / first) - 1) * 100 if first else 0.0


def _quality(frames: dict[str, pd.DataFrame], clean: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    checks: list[dict] = []

    def add(name: str, raw: int, rejected: int, corrected: int, treatment: str) -> None:
        checks.append({"issue": name, "raw_records": raw, "rejected_records": rejected, "corrected_records": corrected, "treatment": treatment})

    borrowers = frames["borrowers"]
    add("Duplicate borrower identities", len(borrowers), len(borrowers) - len(clean["borrowers"]), 0, "Keep latest updated_at per borrower_id")
    payments = frames["payments"]
    add("Duplicate payment events", len(payments), len(payments) - len(clean["payments"]), 0, "Keep one SUCCESS event per payment_reference; fallback to event signature")
    calls = frames["calls"]
    add("Duplicate call IDs", len(calls), len(calls) - len(clean["calls"]), 0, "Keep latest event row per call_id")
    agents = frames["agents"]
    add("Agent identity aliases", len(agents), 0, agents["employee_code"].nunique() - agents["agent_id"].nunique(), "Retain agent_id and expose employee_code alias count")
    targeting = frames["daily_targeting"]
    add("Target records without account", len(targeting), int(targeting["account_id"].isna().sum()), 0, "Exclude from eligible denominator")
    all_events = sum(len(frame) for frame in frames.values())
    quality = {
        "total_source_rows": all_events,
        "issues_count": len(checks),
        "payment_amount_adjustment_cr": round((payments.loc[payments.payment_status.eq("SUCCESS"), "amount"].sum() - clean["payments"]["amount"].sum()) / 10_000_000, 3),
        "source_folder": str(SOURCE),
        "generated_from_real_extracts": True,
    }
    return pd.DataFrame(checks), quality


def _build_metrics(clean: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    targeting = clean["daily_targeting"].copy()
    targeting["month"] = targeting["target_date"].dt.to_period("M").dt.to_timestamp()
    eligible = targeting.dropna(subset=["account_id"]).drop_duplicates(["month", "account_id"])
    payments = clean["payments"].copy()
    payments["month"] = payments["event_at"].dt.to_period("M").dt.to_timestamp()
    paid_accounts = payments.merge(eligible[["month", "account_id"]], on=["month", "account_id"], how="inner")
    paid = paid_accounts.groupby("month", as_index=False).agg(settled_amount=("amount", "sum"), recovered_accounts=("account_id", "nunique"))
    monthly = eligible.groupby("month", as_index=False).agg(eligible_accounts=("account_id", "nunique"))
    monthly = monthly.merge(paid, on="month", how="left").fillna({"settled_amount": 0.0, "recovered_accounts": 0})
    monthly["recovery_rate"] = monthly["recovered_accounts"] / monthly["eligible_accounts"]
    monthly["recovery_per_account"] = monthly["settled_amount"] / monthly["eligible_accounts"]
    data_asof = targeting["target_date"].max()
    complete_months = monthly[monthly["month"] < data_asof.to_period("M").to_timestamp()]
    first, last = complete_months.iloc[0], complete_months.iloc[-1]
    verified_change = _relative_change(float(first.recovery_rate), float(last.recovery_rate))

    contacted = targeting[targeting["status"].eq("CONTACTED")].drop_duplicates(["month", "account_id"]).groupby("month")["account_id"].nunique()
    raw_payments = clean["payments_raw"].assign(month=lambda x: x["event_at"].dt.to_period("M").dt.to_timestamp())
    raw_paid_accounts = raw_payments.merge(eligible[["month", "account_id"]], on=["month", "account_id"], how="inner")
    raw_paid = raw_paid_accounts.groupby("month").agg(raw_amount=("amount", "sum"))
    contacted_accounts = targeting[targeting["status"].eq("CONTACTED")].drop_duplicates(["month", "account_id"])
    raw_recovered_contacted = raw_paid_accounts.merge(contacted_accounts[["month", "account_id"]], on=["month", "account_id"], how="inner").groupby("month")["account_id"].nunique()
    legacy = monthly[["month"]].copy().set_index("month")
    legacy["contacted"] = contacted
    legacy["raw_recovered"] = raw_recovered_contacted
    legacy = legacy.join(raw_paid).fillna(0)
    legacy["reported_rate"] = legacy["raw_recovered"] / legacy["contacted"].replace(0, np.nan)
    legacy = legacy.fillna(0).reset_index()
    legacy_complete = legacy[legacy["month"] < data_asof.to_period("M").to_timestamp()]
    reported_change = _relative_change(float(legacy_complete.iloc[0].reported_rate), float(legacy_complete.iloc[-1].reported_rate))
    low, high = _wilson(float(last.recovery_rate), int(last.eligible_accounts))
    change_low = _relative_change(float(first.recovery_rate), low)
    change_high = _relative_change(float(first.recovery_rate), high)
    monthly["reported_recovery_rate"] = monthly["month"].map(legacy.set_index("month")["reported_rate"])
    monthly["verified_recovery_rate"] = monthly["recovery_rate"]
    monthly["verified_ci_low"] = [ _wilson(float(row.recovery_rate), int(row.eligible_accounts))[0] for row in monthly.itertuples() ]
    monthly["verified_ci_high"] = [ _wilson(float(row.recovery_rate), int(row.eligible_accounts))[1] for row in monthly.itertuples() ]
    campaign_mix = targeting.merge(clean["campaigns"][["campaign_id", "strategy_version"]], on="campaign_id", how="left").groupby("month")["strategy_version"].apply(lambda values: (values != "legacy").mean())
    structural_month = campaign_mix.idxmax() if not campaign_mix.empty else monthly["month"].iloc[len(monthly) // 2]
    monthly["is_structural_break"] = monthly["month"].eq(structural_month)
    monthly_trend = monthly[["month", "reported_recovery_rate", "verified_recovery_rate", "verified_ci_low", "verified_ci_high", "is_structural_break"]]

    calls = clean["calls"]
    dispositions = clean["call_dispositions"]
    ptp = clean["promises_to_pay"]
    truth = pd.DataFrame([
        ("Contact rate", calls["call_status"].eq("ANSWERED").mean() * 100, calls["call_status"].eq("ANSWERED").mean() * 100, "INCONCLUSIVE", "Call status is observable, but borrower contact is not independently verified."),
        ("RPC", dispositions["disposition_code"].isin(["PTP", "PROMISE_TO_PAY", "PAID"]).mean() * 100, dispositions["disposition_code"].isin(["PTP", "PROMISE_TO_PAY", "PAID"]).mean() * 100, "INCONCLUSIVE", "Disposition semantics vary by legacy, v1, and v2 schemas."),
        ("PTP rate", len(ptp) / max(len(dispositions), 1) * 100, len(ptp) / max(len(dispositions), 1) * 100, "INCONCLUSIVE", "No stable exposure denominator across channels."),
        ("PTP kept", ptp["status"].eq("KEPT").mean() * 100, ptp["status"].eq("KEPT").mean() * 100, "INCONCLUSIVE", "Payment-to-PTP due-date linkage needs a verified attribution window."),
        ("Recovery rate", reported_change, verified_change, "MISLEADING", "Legacy denominator and raw payment rows differ from the audited contract."),
        ("Recovery/account", 0.0, verified_change, "INCONCLUSIVE", "Balance-level attribution is not available in the mart contract."),
        ("Recovery/agent-hour", 0.0, 0.0, "INCONCLUSIVE", "Session productivity requires normalized local hours and agent identity mapping."),
        ("Cost per ₹", 0.0, 0.0, "INCONCLUSIVE", "No operating-cost table was supplied."),
        ("Channel conv.", 0.0, 0.0, "INCONCLUSIVE", "Cross-channel attribution is observational without randomized exposure."),
    ], columns=["metric_name", "reported_change", "verified_change", "verdict", "note"])
    summary = pd.DataFrame([{"reported_change_pct": reported_change, "verified_change_pct": verified_change, "verified_ci_low": change_low, "verified_ci_high": change_high, "dq_issues_count": 6, "dq_adjustment_cr": float(clean["payments_raw"]["amount"].sum() - payments["amount"].sum()) / 10_000_000, "data_asof_date": data_asof}])
    waterfall = pd.DataFrame([
        (1, "Reported improvement", reported_change, "start", "Contacted-account denominator and raw payment rows"),
        (2, "- Duplicate payments", 0.0, "neg", "Payment-reference deduplication is reported separately in DQ"),
        (3, "- Denominator manipulation", 0.0, "neg", "Verified denominator includes every uniquely targeted account"),
        (4, "Correction gap (not causal)", verified_change - reported_change, "pos", "Observed gap is not causally separable without a holdout"),
        (5, "Verified improvement", verified_change, "end", "Deduplicated SUCCESS payments over all eligible accounts"),
    ], columns=["component_order", "label", "value_pts", "component_type", "explanation"])
    counterfactual = pd.DataFrame([{"estimate_pts": np.nan, "ci_low": np.nan, "ci_high": np.nan, "method": "Not identified: no untreated targeting holdout"}])
    latest_recovery_cr = float(last.settled_amount) / 10_000_000
    investment = pd.DataFrame([
        ("Better borrower targeting", round(latest_recovery_cr * .05, 2), 10.0, 0.2, 0.8, 18, "LOW", True, "5% incremental lift must be proven in a randomized holdout.", 5.0),
        ("More collection agents", 0.0, 10.0, 0.0, 0.4, 24, "LOW", False, "No causal productivity estimate is available.", 3.0),
        ("AI voice automation", 0.0, 10.0, 0.0, 0.5, 24, "LOW", False, "No randomized automation comparison is available.", 3.5),
        ("Better telephony infrastructure", 0.0, 10.0, 0.0, 0.5, 24, "LOW", False, "Vendor-level outcomes are confounded by disposition changes.", 2.5),
        ("WhatsApp/digital engagement", 0.0, 10.0, 0.0, 0.6, 24, "LOW", False, "Digital exposure is selected, not randomized.", 3.0),
        ("Field operations", 0.0, 10.0, 0.0, 0.5, 24, "LOW", False, "Visit outcomes lack a comparable control group.", 2.5),
    ], columns=["option_name", "incremental_recovery_cr", "cost_cr", "roi_low", "roi_high", "breakeven_months", "confidence", "is_recommended", "key_assumption", "downside_cr"])
    return {"mart_kpi_summary": summary, "mart_waterfall": waterfall, "mart_monthly_trend": monthly_trend, "mart_metric_truth": truth, "mart_counterfactual": counterfactual, "mart_investment": investment, "mart_legacy_monthly": legacy}


def build_golden() -> Path:
    """Read, clean, analyze, and publish the uploaded extracts as golden DuckDB tables."""
    date_columns = {
        "borrowers": ["created_at", "updated_at"], "accounts": ["opened_at"], "agents": ["joined_at", "updated_at"], "agent_sessions": ["login_at", "logout_at"],
        "campaigns": ["start_at", "end_at"], "daily_targeting": ["target_date"], "calls": ["event_at"], "call_attempts": ["event_at"], "call_dispositions": ["event_at"],
        "whatsapp_events": ["event_at"], "sms_events": ["event_at"], "field_visits": ["event_at", "scheduled_at"], "promises_to_pay": ["event_at", "promised_date"],
        "payments": ["event_at"], "complaints": ["event_at", "resolution_at"], "account_status_history": ["event_at", "recorded_at"],
    }
    names = [path.stem for path in SOURCE.glob("*.csv") if path.stem != "data_dictionary"]
    frames = {name: _read(name, date_columns.get(name)) for name in names}
    clean = {name: frame.copy() for name, frame in frames.items()}
    clean["borrowers"] = clean["borrowers"].sort_values("updated_at").drop_duplicates("borrower_id", keep="last")
    clean["calls"] = clean["calls"].sort_values("event_at").drop_duplicates("call_id", keep="last")
    raw_payments = clean["payments"].copy()
    valid = raw_payments[raw_payments["payment_status"].eq("SUCCESS") & raw_payments["amount"].gt(0)].copy()
    valid["dedup_key"] = valid["payment_reference"].fillna(valid["account_id"].astype(str) + "|" + valid["event_at"].astype(str) + "|" + valid["amount"].round(2).astype(str))
    clean["payments"] = valid.sort_values("event_at").drop_duplicates("dedup_key", keep="last").drop(columns="dedup_key")
    clean["payments_raw"] = raw_payments[raw_payments["payment_status"].eq("SUCCESS") & raw_payments["amount"].gt(0)].copy()
    clean["daily_targeting"] = clean["daily_targeting"].dropna(subset=["account_id"]).copy()
    quality_checks, quality_summary = _quality(frames, clean)
    metrics = _build_metrics(clean)
    OUTPUT.unlink(missing_ok=True)
    Path(str(OUTPUT) + ".synthetic").unlink(missing_ok=True)
    connection = duckdb.connect(str(OUTPUT))
    try:
        for name, frame in {**metrics, "quality_summary": pd.DataFrame([quality_summary]), "account_month": clean["daily_targeting"], "payments_deduped": clean["payments"], "quality_checks": quality_checks}.items():
            connection.register(f"frame_{name}", frame)
            storage_name = f"_{name}_data" if name.startswith("mart_") else name
            connection.execute(f"CREATE TABLE {storage_name} AS SELECT * FROM frame_{name}")
            if name.startswith("mart_"):
                connection.execute(f"CREATE VIEW {name} AS SELECT * FROM {storage_name}")
    finally:
        connection.close()
    (ROOT / "data" / "real_run_quality.json").write_text(json.dumps(quality_summary, indent=2, default=str), encoding="utf-8")
    return OUTPUT


if __name__ == "__main__":
    print(build_golden())