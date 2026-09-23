-- 1. Monthly spending trend
SELECT transaction_month,
  SUM(amount_usd) AS total_spending
FROM transactions
GROUP BY transaction_month
ORDER BY transaction_month;
-- 2. Spending by category
SELECT category,
  SUM(amount_usd) AS total_spending
FROM transactions
GROUP BY category
ORDER BY total_spending DESC;
-- 3. Top merchants
SELECT merchant,
  SUM(amount_usd) AS total_spending,
  COUNT(*) AS transaction_count
FROM transactions
GROUP BY merchant
ORDER BY total_spending DESC
LIMIT 10;
-- 4. International vs domestic spending
SELECT is_international,
  SUM(amount_usd) AS total_spending
FROM transactions
GROUP BY is_international;
-- 5. Account-level spending
SELECT account_id,
  SUM(amount_usd) AS total_spending
FROM transactions
GROUP BY account_id
ORDER BY total_spending DESC;
-- 6. Debit vs credit by month
SELECT transaction_month,
  transaction_type,
  SUM(amount_usd) AS total_amount
FROM transactions
GROUP BY transaction_month,
  transaction_type
ORDER BY transaction_month;
-- 7. Transaction status distribution
SELECT status,
  COUNT(*) AS transaction_count
FROM transactions
GROUP BY status;
-- 8. Day-of-week spending
SELECT day_of_week,
  SUM(amount_usd) AS total_spending
FROM transactions
GROUP BY day_of_week
ORDER BY total_spending DESC;
-- 9. Currency distribution
SELECT currency,
  COUNT(*) AS transaction_count,
  SUM(amount_usd) AS total_usd
FROM transactions
GROUP BY currency;
-- 10. Rolling 3-month average
WITH monthly AS (
  SELECT transaction_month,
    SUM(amount_usd) AS total_spending
  FROM transactions
  GROUP BY transaction_month
)
SELECT transaction_month,
  total_spending,
  AVG(total_spending) OVER (
    ORDER BY transaction_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS rolling_3_month_average
FROM monthly
ORDER BY transaction_month;