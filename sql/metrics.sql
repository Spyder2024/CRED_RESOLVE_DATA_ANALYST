-- DuckDB-compatible independent recovery metrics.
-- The real pipeline publishes these tables in the golden.duckdb main schema.
WITH eligible AS (
    SELECT date_trunc('month', target_date) AS month, account_id
    FROM account_month
    WHERE account_id IS NOT NULL
    GROUP BY 1, 2
), settled AS (
    SELECT date_trunc('month', event_at) AS month, account_id, SUM(amount) AS settled_amount
    FROM payments_deduped
    WHERE amount > 0 AND payment_status = 'SUCCESS'
    GROUP BY 1, 2
)
SELECT e.month,
       COUNT(DISTINCT e.account_id) AS eligible_accounts,
       COUNT(DISTINCT s.account_id) AS recovered_accounts,
       COALESCE(SUM(s.settled_amount), 0) AS settled_amount,
       COUNT(DISTINCT s.account_id) * 1.0 / COUNT(DISTINCT e.account_id) AS recovery_rate,
       COALESCE(SUM(s.settled_amount), 0) / COUNT(DISTINCT e.account_id) AS recovery_per_account
FROM eligible e
LEFT JOIN settled s USING (month, account_id)
GROUP BY 1
ORDER BY 1;
