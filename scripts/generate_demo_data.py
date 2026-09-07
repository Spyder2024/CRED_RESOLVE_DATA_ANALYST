from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(42)
months = pd.date_range("2025-01-01", periods=12, freq="MS")
rows = []
for month in months:
    for account_no in range(1, 251):
        account_id = f"A{account_no:05d}"
        assigned = month + pd.Timedelta(days=int(rng.integers(0, 5)))
        dpd = int(rng.choice([5, 15, 30, 60, 90], p=[.18, .22, .28, .22, .10]))
        channel = rng.choice(["human_call", "whatsapp", "field"], p=[.60, .25, .15])
        attempts = int(rng.poisson(2.2 if month.month < 7 else 2.8))
        recovery_probability = .10 + (.035 if month.month >= 7 else 0) + (.025 if channel == "field" else 0)
        recovered = rng.random() < recovery_probability
        rows.append({"account_id": account_id, "month": month.date(), "assigned_at": assigned, "dpd": dpd, "channel": channel, "attempts": attempts, "eligible": True, "payment_amount": float(rng.integers(800, 8000)) if recovered else 0.0})
accounts = pd.DataFrame(rows)
accounts[["account_id", "month", "assigned_at", "dpd", "channel", "attempts", "eligible"]].to_csv(OUT / "daily_targeting.csv", index=False)
payments = accounts.loc[accounts.payment_amount > 0, ["account_id", "assigned_at", "payment_amount"]].rename(columns={"assigned_at": "paid_at"})
payments["payment_id"] = [f"P{i:07d}" for i in range(len(payments))]
payments = payments[["payment_id", "account_id", "paid_at", "payment_amount"]]
payments = pd.concat([payments, payments.iloc[: max(1, len(payments)//50)]], ignore_index=True)
payments.to_csv(OUT / "payments.csv", index=False)
agent_sessions = pd.DataFrame({"session_id": [f"S{i:06d}" for i in range(1, 1501)], "agent_id": rng.choice(["AG01", "AG02", "AG-02", "AG03"], 1500), "started_at": pd.date_range("2025-01-01", periods=1500, freq="6h"), "ended_at": pd.date_range("2025-01-01 01:00", periods=1500, freq="6h")})
agent_sessions.to_csv(OUT / "agent_sessions.csv", index=False)
print(f"Generated {len(accounts):,} targeting rows and {len(payments):,} payment rows in {OUT}")
