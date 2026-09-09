-- =====================================================================
-- SQL DELIVERABLE 1: DATA CLEANING
-- Database: DuckDB
-- Purpose: Deterministic cleaning, deduplication, and anomaly resolution
-- =====================================================================

-- 1. Deduplicate Borrowers: Resolve SCD updates to latest golden record
CREATE OR REPLACE VIEW clean_borrowers AS
WITH ranked_borrowers AS (
    SELECT 
        borrower_id,
        name,
        phone,
        email,
        city,
        state,
        TRY_CAST(created_at AS TIMESTAMP) AS created_at,
        TRY_CAST(updated_at AS TIMESTAMP) AS updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY borrower_id 
            ORDER BY TRY_CAST(updated_at AS TIMESTAMP) DESC
        ) AS rn
    FROM read_csv_auto('data/collections_30k_dataset (4)/borrowers.csv')
)
SELECT 
    borrower_id,
    name,
    phone,
    email,
    city,
    state,
    created_at,
    updated_at
FROM ranked_borrowers
WHERE rn = 1;


-- 2. Deduplicate Payments: Filter SUCCESS only, deduplicate on payment_reference
CREATE OR REPLACE VIEW clean_payments AS
WITH valid_payments AS (
    SELECT 
        payment_id,
        account_id,
        borrower_id,
        amount,
        payment_method,
        payment_status,
        payment_reference,
        TRY_CAST(event_at AS TIMESTAMP) AS event_at,
        COALESCE(
            payment_reference, 
            account_id || '|' || event_at || '|' || CAST(ROUND(amount, 2) AS VARCHAR)
        ) AS dedup_key
    FROM read_csv_auto('data/collections_30k_dataset (4)/payments.csv')
    WHERE payment_status = 'SUCCESS' 
      AND amount > 0
),
ranked_payments AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY dedup_key 
            ORDER BY event_at DESC
        ) AS rn
    FROM valid_payments
)
SELECT 
    payment_id,
    account_id,
    borrower_id,
    amount,
    payment_method,
    payment_status,
    payment_reference,
    event_at
FROM ranked_payments
WHERE rn = 1;


-- 3. Deduplicate Calls: Preserve latest event row per call_id
CREATE OR REPLACE VIEW clean_calls AS
WITH ranked_calls AS (
    SELECT 
        call_id,
        account_id,
        borrower_id,
        agent_id,
        campaign_id,
        direction,
        vendor_id,
        call_status,
        duration_sec,
        timezone,
        TRY_CAST(event_at AS TIMESTAMP) AS event_at,
        ROW_NUMBER() OVER (
            PARTITION BY call_id 
            ORDER BY TRY_CAST(event_at AS TIMESTAMP) DESC
        ) AS rn
    FROM read_csv_auto('data/collections_30k_dataset (4)/calls.csv')
)
SELECT 
    call_id,
    account_id,
    borrower_id,
    agent_id,
    campaign_id,
    direction,
    vendor_id,
    call_status,
    duration_sec,
    timezone,
    event_at
FROM ranked_calls
WHERE rn = 1;


-- 4. Clean Daily Targeting: Exclude records missing account_id
CREATE OR REPLACE VIEW clean_daily_targeting AS
SELECT 
    target_id,
    account_id,
    campaign_id,
    TRY_CAST(target_date AS DATE) AS target_date,
    status AS targeting_status,
    priority,
    recommended_channel
FROM read_csv_auto('data/collections_30k_dataset (4)/daily_targeting.csv')
WHERE account_id IS NOT NULL;
