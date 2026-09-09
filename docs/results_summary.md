# Collections Recovery Analysis Summary

**Run date:** 2026-09-09  
**Source:** `data/collections_30k_dataset (4)`  
**Golden database:** `data/golden.duckdb`  
**Data as of:** 2026-08-08

## Executive verdict

The supplied data does **not** support the business claim that recovery improved by 11% month-on-month.

Using the same complete-month comparison:

| View | Change | Interpretation |
|---|---:|---|
| Legacy contacted-account view | **+4.5%** | The reported-style view after restricting the denominator to contacted accounts and retaining raw successful payment events. |
| Independent audited view | **+31.3%** | Deduplicated positive successful payments divided by all uniquely targeted eligible accounts. |
| Audited uncertainty interval | **+20.4% to +43.1%** | Approximate 95% interval for the audited change. |

The result runs **opposite to the expected assignment narrative**: the audited view is higher than the legacy view. This may reflect denominator construction, portfolio/targeting changes, payment-event defects, or a mismatch between this extract and the historical leadership report. The analysis must not force the data to match the expected story.

August is partial because the latest targeting date is August 8, 2026. It is retained as provisional trend data but excluded from the headline comparison.

## What changed

- Recovery improved in the audited view from the first complete month to the last complete month.
- The legacy view improved less than the audited view.
- The dashboard currently identifies a **26.8 percentage-point gap** between those two relative-change estimates.
- The gap is an observed reconciliation difference, not a causal estimate.

## Data-quality findings

| Issue | Evidence | Treatment | Business impact |
|---|---:|---|---|
| Borrower identity duplicates | 30,600 source rows; 19,585 duplicate rows removed | Keep the latest `updated_at` row per `borrower_id` | Prevents duplicated borrower attributes from influencing joins and segmentation. |
| Payment-event duplicates and invalid statuses | 25,500 source rows; 9,886 rows removed from the audited payment set | Keep positive `SUCCESS` events; deduplicate by `payment_reference`, with account/event/amount fallback | Prevents failed, pending, reversed, and repeated payment events from inflating recovery. |
| Duplicate call IDs | 1,350 duplicate rows | Keep the latest `event_at` per `call_id` | Prevents repeated calls from inflating operational activity. |
| Agent identity aliases | 1,000 agent IDs and 1,099 employee codes; 99 excess aliases | Preserve both identifiers; do not make an unsafe identity collapse | Agent-level productivity remains lower confidence until identity mapping is confirmed. |
| Multiple timezones | UTC, Asia/Kolkata, Asia/Dubai | Retain source timezone; local-hour analysis remains inconclusive | Calling-time and vendor comparisons should not be used for investment decisions yet. |
| Partial final month | Data ends August 8 | Exclude August from headline comparison | Avoids mistaking truncation for a recovery decline. |

The current quality reconciliation estimates approximately **₹17.21 Cr** of gross payment amount difference between raw positive successful events and the deduplicated audited payment set. This is a reconciliation amount, not automatically lost recovery.

## Metric truth

| Metric | Reported change | Verified change | Verdict |
|---|---:|---:|---|
| Contact rate | +19.9% | +19.9% | Inconclusive |
| RPC | +33.3% | +33.3% | Inconclusive |
| PTP rate | +51.4% | +51.4% | Inconclusive |
| PTP kept | +24.9% | +24.9% | Inconclusive |
| Recovery rate | +4.5% | **+31.3%** | Misleading legacy denominator |
| Recovery/account | 0.0% | +31.3% | Inconclusive |
| Recovery/agent-hour | 0.0% | 0.0% | Inconclusive |
| Cost per ₹ recovered | 0.0% | 0.0% | Inconclusive |
| Channel conversion | 0.0% | 0.0% | Inconclusive |

Only the recovery-rate comparison is currently classified as misleading. The other metrics should not be treated as proven because the supplied extract lacks stable attribution, cost, exposure, or identity controls for them.

## Why confidence is limited

The following analyses cannot be identified reliably from the supplied extract alone:

- A targeting counterfactual: there is no untreated targeting holdout.
- Causal channel lift: channel exposure is observational and selected.
- Recovery per agent-hour: session duration and agent identity normalization require further validation.
- Cost per rupee recovered: no operating-cost table was supplied.
- Robust PTP-kept attribution: payment-to-PTP due-date matching and attribution windows need a documented contract.

## ₹10 Cr recommendation

### Recommend: better borrower targeting as a low-confidence pilot

This is a **pilot recommendation, not approval for an unconditional ₹10 Cr rollout**.

| Measure | Current model |
|---|---:|
| Modeled incremental recovery | **₹0.18 Cr** |
| Investment cost | ₹10 Cr |
| Modeled ROI range | 0.2x–0.8x |
| Modeled break-even | 18 months |
| Downside at risk | ₹5.0 Cr |
| Confidence | LOW |

The model assumes a 5% incremental lift. That assumption is not established by the uploaded data.

### Required experiment before scaling

1. Randomly assign approximately 10% of eligible accounts to a control group.
2. Keep portfolio mix, DPD, client, geography, borrower segment, and collection capacity balanced.
3. Preserve the fixed account-month denominator and payment deduplication rules.
4. Run the experiment for at least two complete collection months.
5. Measure incremental settled amount, recovery rate, PTP kept rate, complaints, and cost.
6. Scale only if the confidence interval for incremental recovery excludes zero and complaint rates do not worsen.

## Reproducibility

Build the real golden database:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.pipeline
```

Run the dashboard:

```powershell
streamlit run .\dashboard\app.py
```

The dashboard reads from `data/golden.duckdb`. The uploaded source files remain under `data/collections_30k_dataset (4)`. Generated DuckDB artifacts are intentionally ignored by Git and can be recreated from the source extracts.
