-- PostgreSQL 14+. Synthetic transactions only.
CREATE TABLE IF NOT EXISTS fraud_transactions (
 transaction_id TEXT PRIMARY KEY, event_time TIMESTAMP, amount_ngn NUMERIC(16,2),
 prior_24h_transactions INT, new_device INT, cross_border INT,
 hour_of_day INT, is_fraud INT
);
-- Load using psql: \copy fraud_transactions FROM 'data/transactions.csv' CSV HEADER
-- Label is available for retrospective evaluation, NEVER as a prediction feature.
SELECT date_trunc('month',event_time)::date AS month,
 COUNT(*) AS transactions, SUM(is_fraud) AS actual_fraud_cases,
 ROUND(AVG(is_fraud::numeric)*100,2) AS fraud_rate_pct,
 ROUND(SUM(CASE WHEN is_fraud=1 THEN amount_ngn ELSE 0 END),2) AS observed_fraud_value_ngn
FROM fraud_transactions GROUP BY 1 ORDER BY 1;
SELECT new_device,cross_border,COUNT(*) AS transactions,
 SUM(is_fraud) AS fraud_cases,ROUND(AVG(is_fraud::numeric)*100,2) AS fraud_rate_pct
FROM fraud_transactions GROUP BY 1,2 ORDER BY fraud_rate_pct DESC;
-- Rules-based alert review queue for comparison against the ML experiment.
SELECT transaction_id,event_time,amount_ngn,
 CASE WHEN new_device=1 AND amount_ngn>230000 THEN 'Review' ELSE 'Standard' END AS rule_alert
FROM fraud_transactions ORDER BY event_time;
