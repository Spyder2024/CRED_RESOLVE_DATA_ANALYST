-- DuckDB-compatible independent recovery metrics.
-- Run after registering CSV/parquet sources in the orchestration layer.
WITH eligible AS (
    SELECT month, account_id
    FROM golden.account_month
    WHERE eligible = TRUE
    QUALIFY ROW_NUMBER() OVER (PARTITION BY month, account_id ORDER BY assigned_at DESC) = 1
), settled AS (
    SELECT date_trunc('month', paid_at) AS month, account_id, SUM(payment_amount) AS settled_amount
    FROM golden.payments_deduped
    WHERE payment_amount > 0
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
