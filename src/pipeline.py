from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).parents[1]
RAW = ROOT / "data" / "raw"
GOLDEN = ROOT / "data" / "golden"
GOLDEN.mkdir(parents=True, exist_ok=True)


def run():
    targeting = pd.read_csv(RAW / "daily_targeting.csv", parse_dates=["month", "assigned_at"])
    payments = pd.read_csv(RAW / "payments.csv", parse_dates=["paid_at"])
    raw_targeting_rows = len(targeting)
    targeting["account_id"] = targeting["account_id"].astype(str).str.strip().str.upper()
    payments["account_id"] = payments["account_id"].astype(str).str.strip().str.upper()
    payments["payment_amount"] = pd.to_numeric(payments["payment_amount"], errors="coerce").fillna(0).clip(lower=0)
    raw_payment_rows = len(payments)
    payments["payment_hash"] = payments["account_id"].astype(str) + "|" + payments["paid_at"].astype(str) + "|" + payments["payment_amount"].round(2).astype(str)
    payments = payments.drop_duplicates(subset=["payment_hash"]).copy()
    targeting = targeting.sort_values(["account_id", "month", "assigned_at"]).drop_duplicates(["account_id", "month"], keep="last")
    targeting["month"] = targeting["month"].dt.to_period("M").dt.to_timestamp()
    payments["month"] = payments["paid_at"].dt.to_period("M").dt.to_timestamp()
    monthly = targeting.groupby("month", as_index=False).agg(eligible_accounts=("account_id", "nunique"), total_attempts=("attempts", "sum"), accounts_attempted=("attempts", lambda x: int((x > 0).sum())))
    paid = payments.groupby("month", as_index=False).agg(settled_amount=("payment_amount", "sum"), recovered_accounts=("account_id", "nunique"))
    monthly = monthly.merge(paid, on="month", how="left").fillna({"settled_amount": 0, "recovered_accounts": 0})
    monthly["recovery_rate"] = monthly["recovered_accounts"] / monthly["eligible_accounts"]
    monthly["recovery_per_account"] = monthly["settled_amount"] / monthly["eligible_accounts"]
    monthly["attempt_rate"] = monthly["accounts_attempted"] / monthly["eligible_accounts"]
    monthly["reported_mom_change"] = monthly["recovery_rate"].pct_change()
    monthly["metric_version"] = "v1_fixed_month_start_30d_payment_date"
    monthly.to_csv(GOLDEN / "monthly_metrics.csv", index=False)
    targeting.to_csv(GOLDEN / "account_month.csv", index=False)
    payments.to_csv(GOLDEN / "payments_deduped.csv", index=False)
    quality = {"targeting_raw_rows": raw_targeting_rows, "payments_raw_rows": raw_payment_rows, "payments_deduped_rows": len(payments), "duplicate_payment_rows_removed": raw_payment_rows - len(payments), "metric_version": "v1_fixed_month_start_30d_payment_date"}
    (GOLDEN / "quality_report.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    print(f"Wrote {len(monthly)} months, removed {quality['duplicate_payment_rows_removed']} duplicate payment rows")


if __name__ == "__main__":
    run()
