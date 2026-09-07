# Data quality report

## Current run

The current run uses synthetic demo data because the workspace contains only the assignment PDF. This is a pipeline validation result, not a business finding.

| Check | Detection | Treatment | Demo impact |
|---|---|---|---:|
| Duplicate payments | Account + paid timestamp + amount hash | Keep one row | 6 rows removed |
| Duplicate account-month targeting | Account/month uniqueness | Keep latest assigned event | Applied before aggregation |
| Negative or invalid payments | Numeric coercion and lower bound | Convert invalid to zero; flag in production | None observed |
| Missing payment months | Left join to eligible population | Fill settled amount and recovered accounts with zero | Preserves denominator |
| Agent identity aliases | Canonical mapping table required | Map AG-02 to AG02 in production staging | Demo sessions include alias |
| Time zones | Source-local timestamp plus source timezone required | Convert to UTC, derive business local date | Not inferable from demo |

## Production acceptance gates

Block publication when payment keys are not unique after deduplication, eligible-account counts fall unexpectedly, monetary totals become negative, or more than 1% of events lack a usable timestamp. Warnings should be visible on the dashboard rather than silently dropping rows.

## Business impact to quantify with real data

1. Recovery rate before and after payment deduplication.
2. Recovery rate using latest-interaction attribution versus payment-date attribution.
3. Denominator change from all assigned accounts versus surviving contacted accounts.
4. Month and channel impact of timezone normalization.
5. Share of agents resolved through alias mapping.
