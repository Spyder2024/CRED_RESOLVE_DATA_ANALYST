-- =====================================================================
-- SQL DELIVERABLE 4: MULTI-DIMENSIONAL ANALYTICAL QUERIES
-- Database: DuckDB
-- Purpose: Dimensional driver investigation and counterfactual analysis
-- =====================================================================

-- 1. Recovery Performance by Days Past Due (DPD) Buckets
CREATE OR REPLACE VIEW mart_recovery_by_dpd AS
WITH account_dpd AS (
    SELECT 
        a.account_id,
        a.dpd,
        CASE 
            WHEN a.dpd < 30 THEN '1. DPD < 30'
            WHEN a.dpd BETWEEN 30 AND 59 THEN '2. DPD 30-59'
            WHEN a.dpd BETWEEN 60 AND 89 THEN '3. DPD 60-89'
            ELSE '4. DPD 90+'
        END AS dpd_bucket,
        a.outstanding_amount
    FROM read_csv_auto('data/collections_30k_dataset (4)/accounts.csv') a
)
SELECT 
    d.dpd_bucket,
    COUNT(DISTINCT c.account_id) AS total_assigned_accounts,
    COUNT(DISTINCT CASE WHEN c.is_recovered = 1 THEN c.account_id END) AS recovered_accounts,
    ROUND(COUNT(DISTINCT CASE WHEN c.is_recovered = 1 THEN c.account_id END) * 1.0 / 
          COUNT(DISTINCT c.account_id), 4) AS recovery_rate,
    ROUND(SUM(c.settled_amount), 2) AS total_settled_amount,
    ROUND(AVG(d.outstanding_amount), 2) AS avg_outstanding_amount
FROM fct_account_cohort_recovery c
JOIN account_dpd d ON c.account_id = d.account_id
GROUP BY 1
ORDER BY 1;


-- 2. Recovery Performance by Outreach Channel
CREATE OR REPLACE VIEW mart_recovery_by_channel AS
SELECT 
    primary_channel,
    COUNT(DISTINCT account_id) AS total_accounts,
    COUNT(DISTINCT CASE WHEN is_recovered = 1 THEN account_id END) AS recovered_accounts,
    ROUND(COUNT(DISTINCT CASE WHEN is_recovered = 1 THEN account_id END) * 1.0 / 
          COUNT(DISTINCT account_id), 4) AS recovery_rate,
    ROUND(SUM(settled_amount), 2) AS total_settled_amount
FROM fct_account_cohort_recovery
GROUP BY 1
ORDER BY recovery_rate DESC;


-- 3. Telephony Performance by Vendor & Timezone
CREATE OR REPLACE VIEW mart_vendor_call_performance AS
SELECT 
    vendor_id,
    timezone,
    COUNT(DISTINCT call_id) AS total_call_attempts,
    COUNT(DISTINCT CASE WHEN call_status = 'ANSWERED' THEN call_id END) AS answered_calls,
    ROUND(COUNT(DISTINCT CASE WHEN call_status = 'ANSWERED' THEN call_id END) * 1.0 / 
          COUNT(DISTINCT call_id), 4) AS answer_rate,
    ROUND(AVG(duration_sec), 1) AS avg_duration_seconds
FROM clean_calls
GROUP BY 1, 2
ORDER BY vendor_id, answer_rate DESC;


-- 4. Calling Time of Day Distribution (Hourly Call Volume & Connection)
CREATE OR REPLACE VIEW mart_calling_hour_distribution AS
SELECT 
    EXTRACT(HOUR FROM event_at) AS call_hour,
    COUNT(DISTINCT call_id) AS call_volume,
    COUNT(DISTINCT CASE WHEN call_status = 'ANSWERED' THEN call_id END) AS answered_volume,
    ROUND(COUNT(DISTINCT CASE WHEN call_status = 'ANSWERED' THEN call_id END) * 1.0 / 
          COUNT(DISTINCT call_id), 4) AS hourly_answer_rate
FROM clean_calls
GROUP BY 1
ORDER BY call_hour;


-- 5. Targeting Counterfactual: Pre-change vs Post-change Cohort Comparison
CREATE OR REPLACE VIEW mart_targeting_counterfactual_comparison AS
WITH campaign_strategy AS (
    SELECT 
        c.campaign_id,
        c.strategy_version,
        TRY_CAST(c.start_at AS TIMESTAMP) AS start_at
    FROM read_csv_auto('data/collections_30k_dataset (4)/campaigns.csv') c
),
account_strategy AS (
    SELECT 
        t.account_id,
        t.target_date,
        s.strategy_version
    FROM clean_daily_targeting t
    JOIN campaign_strategy s ON t.campaign_id = s.campaign_id
)
SELECT 
    a.strategy_version,
    COUNT(DISTINCT f.account_id) AS cohort_accounts,
    COUNT(DISTINCT CASE WHEN f.is_recovered = 1 THEN f.account_id END) AS recovered_accounts,
    ROUND(COUNT(DISTINCT CASE WHEN f.is_recovered = 1 THEN f.account_id END) * 1.0 / 
          COUNT(DISTINCT f.account_id), 4) AS observed_recovery_rate,
    ROUND(SUM(f.settled_amount), 2) AS total_settled_amount
FROM fct_account_cohort_recovery f
JOIN account_strategy a ON f.account_id = a.account_id
GROUP BY 1
ORDER BY a.strategy_version;
