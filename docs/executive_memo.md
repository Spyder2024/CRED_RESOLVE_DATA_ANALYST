# Executive Memorandum: Collections Recovery Forensics & ₹10 Cr Capital Advisory

**To:** Executive Leadership Team  
**From:** Lead Analytics & Forensics Auditor  
**Date:** September 10, 2026  
**Subject:** Verification of +11% Recovery Claim, Operational Diagnostic, and Capital Allocation Recommendation  

---

### 1. What Happened?
The widely circulated claim that *"Recovery has improved by 11% month-on-month"* **does not survive independent audit**. 

- **Audited Performance:** Across the seven complete months in the primary dataset (January 1 – July 31, 2026), the independently audited recovery rate grew from **14.2% to 24.8%**—an overall increase of **+31.3%** ($95\%\text{ CI: }+20.4\%\text{ to }+43.1\%$).
- **Legacy Reconstruction:** Under the historical reported-style calculation (which restricted the denominator solely to agent-contacted accounts and included duplicate payment callbacks), recovery grew by only **+4.5%**.
- **Definition Gap:** There is a **+26.8 percentage-point gap** between the audited view and the legacy view. Rather than overstating recovery, historical reporting actually **severely understated true collections performance** due to denominator distortion.
- **Data Truncation Alert:** Data for August 2026 cuts off on August 8. It has been isolated as provisional trend data and excluded from headline growth calculations to prevent mistaking truncation for operational failure.

---

### 2. Why Did It Happen?
Our forensic decomposition reveals three root drivers for the observed trajectory:

1. **Denominator Distortion (Fact):** Legacy metrics tracked conversion exclusively against accounts successfully contacted by dialers ($N \approx 800–1,200$/month). This excluded the massive surge in autonomous digital repayments (WhatsApp links, automated SMS, mobile UPI intents), which accounted for over 45% of total settled recoveries. Auditing the entire assigned eligible cohort ($N \approx 3,000–3,500$/month) captures these true receipts.
2. **Transaction Deduplication (Fact):** The raw dataset contained 9,886 redundant payment records caused by webhook retries, totaling **₹17.21 Cr**. Deduplicating by `payment_reference` normalized accounting ledgers without changing verified cash collections.
3. **Favorable Risk Mix Shift (Strong Evidence):** The portfolio mix experienced early-bucket migration, with DPD 30–59 accounts increasing from 34.2% to 39.8% of assigned volume. Fresher delinquencies cure at inherently higher rates regardless of outreach channel.
4. **Targeting Model Impact (Hypothesis):** While collections increased following the mid-year rollout of v2 borrower targeting, the lack of an untreated holdout means this cannot be causally separated from concurrent digital adoption and portfolio mix shifts.

---

### 3. How Confident Are We?
- **Audited Recovery Trajectory: HIGH CONFIDENCE.** The audited increase of +31.3% is verified by immutable DuckDB golden marts and supported by a robust 95% bootstrap confidence interval ($[+20.4\%, +43.1\%]$) that strictly excludes both zero and the legacy +4.5% baseline.
- **Headline Discrepancy: HIGH CONFIDENCE.** The ₹17.21 Cr reconciliation amount is proven to be gateway retry duplication rather than cash leakage.
- **Operational Metrics: LOW CONFIDENCE / INCONCLUSIVE.** Seven key operating metrics (Collector Productivity per Agent-Hour, Cost per Rupee Recovered, RPC, PTP Kept Rate, Channel Conversion) remain inconclusive due to incomplete agent alias bridges (1,000 IDs vs 1,099 employee codes) and unintegrated vendor telephony cost tables.
- **Causal Targeting Lift: LOW CONFIDENCE.** Without an A/B experimental baseline, treatment assignment is confounded by borrower risk propensity.

---

### 4. What Should We Do?
Leadership must **NOT** authorize an immediate, unconditional ₹10 Cr full-scale rollout for borrower targeting. 

Instead, recommend **authorizing Better Borrower Targeting exclusively as a Controlled ₹10 Cr Phased Pilot**:

1. **Establish a Strict 10% Randomized Holdout:** Prior to targeting model execution, isolate a randomized 10% control group within the eligible universe via deterministic hashing.
2. **Pre-Register Core Primary Outcomes:** Pre-register net settled recovery, borrower contact fatigue, and regulatory complaint frequency across a 60-day trial (spanning two complete settlement cycles).
3. **Integrate Operational Telemetry:** Require dialer vendor cost files and HR employee alias maps to be integrated into staging before evaluating operational productivity.
4. **Enforce Go/No-Go Gate:** Only release subsequent capital tranches if the lower bound of the empirical treatment lift exceeds the required hurdle ROI ($1.5\times$).

---

### 5. What is the Expected Financial Impact?

| Financial & Risk Metric | Current Modeled Expectation | Sensitivity & Boundary Range |
| :--- | :---: | :--- |
| **Capital Outlay** | **₹10.00 Cr** | Phased tranches ($₹2.0\text{ Cr pilot} \rightarrow ₹8.0\text{ Cr scale}$) |
| **Expected Incremental Recovery** | **₹0.18 Cr** | Assuming base-case 5.0% incremental lift over baseline |
| **Expected Net ROI** | **0.2× – 0.8×** | Sub-par return under observational assumptions |
| **Breakeven Horizon** | **18 Months** | Range: 12 to 24 months |
| **Maximum Downside at Risk** | **₹5.00 Cr** | Capital at risk if targeting model degrades cure rates or increases churn |
| **Recommendation Confidence** | **LOW** | Observational correlation only; requires RCT validation |

**Executive Conclusion:** Operating performance is genuinely improving (+31.3% audited recovery), but the headline 11% claim is disproven. Protecting shareholder capital requires validating targeting causality through a holdout pilot before deploying the full ₹10 Cr.
