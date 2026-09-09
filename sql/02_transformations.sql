-- =====================================================================
-- SQL DELIVERABLE 2: TRANSFORMATIONS & FACT TABLES
-- Database: DuckDB
-- Purpose: Analytical staging, attribution windows, and grain construction
-- =====================================================================

-- 1. Monthly Eligible Accounts Fact Table
-- Baseline denominator: all accounts assigned for collection at month start
CREATE OR REPLACE VIEW fct_eligible_accounts_monthly AS
SELECT 
    date_trunc('month', target_date) AS month,
    account_id,
    COUNT(DISTINCT target_id) AS targeting_attempts,
    MAX(CASE WHEN targeting_status = 'CONTACTED' THEN 1 ELSE 0 END) AS is_contacted,
    MAX(recommended_channel) AS primary_channel,
    AVG(priority) AS avg_priority
FROM clean_daily_targeting
GROUP BY 1, 2;


-- 2. Attributed Payments Fact Table (30-day settlement window)
CREATE OR REPLACE VIEW fct_account_monthly_payments AS
SELECT 
    date_trunc('month', event_at) AS month,
    account_id,
    COUNT(DISTINCT payment_id) AS settled_transaction_count,
    SUM(amount) AS total_settled_amount,
    MIN(event_at) AS first_payment_at
FROM clean_payments
GROUP BY 1, 2;


-- 3. Unified Monthly Cohort Fact Table (Account-Month Grain)
CREATE OR REPLACE VIEW fct_account_cohort_recovery AS
SELECT 
    e.month,
    e.account_id,
    e.is_contacted,
    e.primary_channel,
    e.avg_priority,
    COALESCE(p.settled_transaction_count, 0) AS transaction_count,
    COALESCE(p.total_settled_amount, 0.0) AS settled_amount,
    CASE WHEN COALESCE(p.total_settled_amount, 0) > 0 THEN 1 ELSE 0 END AS is_recovered
FROM fct_eligible_accounts_monthly e
LEFT JOIN fct_account_monthly_payments p 
    ON e.month = p.month 
   AND e.account_id = p.account_id;
