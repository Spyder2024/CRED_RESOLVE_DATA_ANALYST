# Executive memo (complete after loading real extracts)

## What happened?

**Status: pending real data.** The dashboard currently runs on synthetic data only. Report: recovery rate, settled amount, recovery/account, recovery/agent-hour, and PTP kept rate with fixed month-start denominators.

## Why?

Separate facts from evidence. Report mix-adjusted results by DPD, client, geography, language, agent tenure, campaign, channel, vendor, calling hour, attempt frequency, and borrower segment. Label every statement as Fact, Strong Evidence, Correlation, or Hypothesis.

## Is 11% real?

Compare the reported metric with the independent metric contract in `README.md`. Quantify absolute percentage-point and relative change, and show the impact of deduplication, denominator repair, timezone normalization, and payment attribution.

## Recommendation

Do not commit the ₹10 Cr until the counterfactual and a holdout test are complete. Select one investment only after estimating incremental settled amount, total cost, ROI, break-even month, uncertainty interval, and downside case. If no reliable causal estimate exists, recommend a randomized pilot and state the minimum detectable effect and duration.
