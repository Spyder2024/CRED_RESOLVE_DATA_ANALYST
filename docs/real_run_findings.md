# Real extract findings

Run date: 2026-09-09

Source: `data/collections_30k_dataset (4)`

## Verdict

The uploaded extract does **not** verify the business statement that recovery improved 11% month-on-month. Using the independent account-month denominator and deduplicated successful payments:

- Legacy contacted-account view: **+4.5%** from the first complete month to the last complete month.
- Audited eligible-account view: **+31.3%** over the same complete months.
- Approximate audited uncertainty interval: **+20.4% to +43.1%**.
- Latest source date: **2026-08-08**. August is partial and remains visible in the trend but is excluded from the headline comparison.

This is the opposite direction from the assignment's expected narrative. It may indicate that the supplied dataset's legacy denominator is more conservative, that its targeting population changed materially, or that the source extract does not represent the historical report used by leadership. It must not be silently forced into the expected 11% story.

## Data forensics

| Issue | Observed treatment |
|---|---|
| Borrower duplicates | Keep latest `updated_at` per `borrower_id`; 30,600 source rows reduced to 11,015 unique IDs. |
| Payment duplicates | Restrict to positive `SUCCESS`; deduplicate non-null `payment_reference`, otherwise account/event/amount signature. |
| Call duplicates | Keep latest `event_at` per `call_id`; 1,350 duplicate rows removed. |
| Agent identities | 1,000 agent IDs and 1,099 employee codes are retained as separate identity attributes; no unsafe collapse was applied. |
| Timezones | UTC, Asia/Kolkata, and Asia/Dubai are present. A timezone-aware local-hour analysis requires a source timezone contract and is marked inconclusive here. |
| Partial month | August 2026 ends on the 8th; excluded from headline change, retained as provisional trend data. |
| Counterfactual | Not identified: there is no untreated targeting holdout. |
| Costs | No operating-cost table was supplied, so cost per rupee and ROI remain low-confidence assumptions. |

## Investment decision

The dashboard selects **better borrower targeting** only as a low-confidence pilot recommendation. Its modeled incremental recovery assumes a 5% lift and must be validated with a randomized holdout. The supplied data alone cannot justify deploying the full ₹10 Cr.
