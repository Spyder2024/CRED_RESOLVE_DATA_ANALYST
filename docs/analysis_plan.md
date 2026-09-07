# Analysis plan

## Causal discipline

Every finding is labeled:

- **Fact:** directly measured after the golden-layer rules.
- **Strong Evidence:** robust across specifications, with timing and dose-response support.
- **Correlation:** associated but not identified as causal.
- **Hypothesis:** plausible explanation requiring an experiment or additional data.

## Required slices

Compute fixed-denominator recovery rate and recovery per account by portfolio mix, DPD, client, geography, language, agent, tenure, campaign, channel, vendor, calling hour, attempt-frequency band, and borrower segment. Report both raw and standardized-to-baseline mix results to separate population change from operational change.

## Counterfactual

Treatment: accounts first exposed after the targeting strategy change. Control: accounts not exposed to the new strategy during the same calendar window, matched on pre-period recovery risk, DPD, client, geography, language, portfolio, and prior attempts. Primary estimand: difference in post-period recovery rate after subtracting the pre-period gap. Check parallel pre-trends, spillovers, selective missingness, and changing collection capacity. A randomized account-level holdout is the preferred confirmatory design.

## ₹10 Cr decision rule

Do not select an investment from observational lift alone. For each option estimate incremental settled rupees, implementation and operating cost, ROI, break-even month, 80% interval, and downside case. Advance only an option with a credible holdout or quasi-experimental estimate and an operational path to measure incremental recovery.
