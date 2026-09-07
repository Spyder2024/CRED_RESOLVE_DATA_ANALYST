# Collections Recovery Forensics

A reproducible answer to the Data Analyst assignment. The project is designed to run first on generated demo data, then on the supplied raw extracts without changing the analytical contracts.

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\generate_demo_data.py
python -m src.pipeline
streamlit run dashboard\app.py
```

The demo data is deliberately small and synthetic. It exercises duplicate payments, multiple agent identifiers, late events, timezone normalization, and a mid-year targeting change. Replace files under `data/raw/` with the supplied extracts and rerun the pipeline.

The executive dashboard is powered exclusively by `data/golden.duckdb`. On a fresh clone, `dashboard/app.py` generates the contract-identical synthetic database automatically. When a real `data/golden.duckdb` is placed there, the dashboard detects it as `GOLDEN` without code changes.

## Repository map

- `data/raw/`: source extracts; never edit in place.
- `data/staging/`: typed, standardized source tables.
- `data/golden/`: deduplicated analytical tables and monthly metrics.
- `src/pipeline.py`: deterministic cleaning, entity resolution, attribution, and metrics.
- `sql/`: dialect-neutral DuckDB SQL for the production metric layer.
- `analysis/recovery_forensics.ipynb`: reasoning and statistical investigation notebook.
- `app.py`: one-screen executive dashboard.
- `docs/`: data-quality report, executive memo template, and production architecture.

## Important status

The assignment PDF contains requirements but no raw datasets. Until the extracts are loaded, no business conclusion is valid. The dashboard labels demo outputs as demo data; replace them before making an investment decision.

## Independent metric contract

- Recovery rate = distinct accounts with a settled payment in the 30-day attribution window / eligible accounts assigned at month start.
- Recovery per account = settled amount / eligible accounts.
- Recovery per agent-hour = settled amount / productive logged-in hours.
- PTP kept rate = distinct PTPs with a payment on or before due date / distinct valid PTPs due in the observation window.
- Cost per rupee recovered = fully loaded operating cost / settled payment amount.

All payment amounts are attributed to the account and payment date, never to the latest interaction. Campaign/channel attribution is a separate exposure table with a fixed 30-day window.
