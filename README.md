# Collections Recovery Forensics

A reproducible answer to the Data Analyst assignment. The project is designed to run first on generated demo data, then on the supplied raw extracts without changing the analytical contracts.

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.pipeline
streamlit run dashboard\app.py
```

The uploaded source package is under `data/collections_30k_dataset (4)/`. It contains 17 CSV extracts and the data dictionary. The real pipeline reads that folder directly; `data/raw/` is intentionally empty.

The executive dashboard is powered exclusively by `data/golden.duckdb`. If that file is absent, it generates a contract-identical synthetic fallback; with the uploaded data present, run `python -m src.pipeline` to create the real database and the dashboard detects it as `GOLDEN`.

The current real-run conclusions are documented in [docs/real_run_findings.md](docs/real_run_findings.md). They are intentionally not forced to match the assignment's suggested narrative: the supplied extract produces a +4.5% legacy change and +31.3% audited change over complete months, with August 8 treated as partial.

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
