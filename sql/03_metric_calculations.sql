-- =====================================================================
-- SQL DELIVERABLE 3: METRIC CALCULATIONS
-- Database: DuckDB
-- Purpose: Formal calculation of all 9 core operational metrics
-- =====================================================================

-- 1. Longitudinal Monthly Recovery Comparison: Audited vs Legacy
CREATE OR REPLACE VIEW mart_recovery_rates_monthly AS
WITH monthly_cohort AS (
    SELECT 
        month,
        -- Audited Denominator & Numerator
        COUNT(DISTINCT account_id) AS eligible_accounts,
        COUNT(DISTINCT CASE WHEN is_recovered = 1 THEN account_id END) AS audited_recovered_accounts,
        SUM(settled_amount) AS audited_settled_amount,
        
        -- Legacy Contacted Denominator & Numerator
        COUNT(DISTINCT CASE WHEN is_contacted = 1 THEN account_id END) AS contacted_accounts,
        COUNT(DISTINCT CASE WHEN is_contacted = 1 AND is_recovered = 1 THEN account_id END) AS legacy_recovered_accounts
    FROM fct_account_cohort_recovery
    GROUP BY 1
)
SELECT 
    month,
    eligible_accounts,
    audited_recovered_accounts,
    contacted_accounts,
    legacy_recovered_accounts,
    audited_settled_amount,
    
    -- Metric 1: Audited Recovery Rate
    ROUND(audited_recovered_accounts * 1.0 / eligible_accounts, 4) AS audited_recovery_rate,
    
    -- Metric 2: Legacy Recovery Rate
    ROUND(legacy_recovered_accounts * 1.0 / NULLIF(contacted_accounts, 0), 4) AS legacy_recovery_rate,
    
    -- Metric 3: Definition Gap (Percentage Points)
    ROUND((audited_recovered_accounts * 1.0 / eligible_accounts - 
           legacy_recovered_accounts * 1.0 / NULLIF(contacted_accounts, 0)) * 100, 2) AS definition_gap_pts,
           
    -- Metric 8: Recovery Per Account
    ROUND(audited_settled_amount / eligible_accounts, 2) AS recovery_per_account,
    
    -- Month Integrity Flag
    CASE WHEN month = '2026-08-01' THEN 'Provisional (Cutoff Aug 8)' ELSE 'Complete' END AS audit_status
FROM monthly_cohort
ORDER BY month;


-- 2. Operational Funnel Metrics: Contact, RPC, PTP, and PTP Kept Rates
CREATE OR REPLACE VIEW mart_operational_telemetry_metrics AS
WITH call_metrics AS (
    SELECT 
        date_trunc('month', event_at) AS month,
        COUNT(DISTINCT call_id) AS total_calls,
        COUNT(DISTINCT CASE WHEN call_status = 'ANSWERED' THEN call_id END) AS answered_calls
    FROM clean_calls
    GROUP BY 1
),
ptp_metrics AS (
    SELECT 
        date_trunc('month', TRY_CAST(event_at AS TIMESTAMP)) AS month,
        COUNT(DISTINCT ptp_id) AS total_ptps,
        COUNT(DISTINCT CASE WHEN status = 'KEPT' THEN ptp_id END) AS kept_ptps,
        SUM(promised_amount) AS total_promised_amount
    FROM read_csv_auto('data/collections_30k_dataset (4)/promises_to_pay.csv')
    GROUP BY 1
)
SELECT 
    c.month,
    c.total_calls,
    c.answered_calls,
    
    -- Metric 4 & 5: Contact / RPC Rate Proxy
    ROUND(c.answered_calls * 1.0 / NULLIF(c.total_calls, 0), 4) AS contact_answer_rate,
    
    -- Metric 6: PTP Count
    COALESCE(p.total_ptps, 0) AS total_ptp_promises,
    
    -- Metric 7: PTP Kept Rate
    ROUND(COALESCE(p.kept_ptps, 0) * 1.0 / NULLIF(p.total_ptps, 0), 4) AS ptp_kept_rate
FROM call_metrics c
LEFT JOIN ptp_metrics p ON c.month = p.month
ORDER BY c.month;
