-- PostgreSQL 14+. No real bank or cardholder information is included.
CREATE TABLE IF NOT EXISTS provider_transactions (
 reference TEXT PRIMARY KEY,payment_time TIMESTAMP,provider TEXT,
 gross_ngn NUMERIC(16,2),fee_ngn NUMERIC(16,2),expected_net_ngn NUMERIC(16,2)
);
CREATE TABLE IF NOT EXISTS bank_credits (
 bank_entry_id TEXT PRIMARY KEY,reference TEXT,posted_at TIMESTAMP,credit_ngn NUMERIC(16,2)
);
-- Load using psql \copy provider_transactions and \copy bank_credits from corresponding CSVs.
WITH credits AS (
 SELECT reference,COUNT(*) AS entries,SUM(credit_ngn) AS credit_total,MIN(posted_at) AS first_posted
 FROM bank_credits GROUP BY reference
), reconciled AS (
 SELECT p.reference,p.provider,p.expected_net_ngn,COALESCE(c.credit_total,0) AS credit_total,
 CASE WHEN c.entries IS NULL THEN 'Missing'
 WHEN c.entries>1 THEN 'Duplicate'
 WHEN ABS(c.credit_total-p.expected_net_ngn)>.01 THEN 'Amount mismatch'
 WHEN c.first_posted-p.payment_time>INTERVAL '24 hours' THEN 'Delayed'
 ELSE 'Matched' END AS recon_status
 FROM provider_transactions p LEFT JOIN credits c ON p.reference=c.reference
)
SELECT provider,recon_status,COUNT(*) AS transactions,
 SUM(ABS(expected_net_ngn-credit_total)) AS abs_variance_ngn
FROM reconciled GROUP BY 1,2 ORDER BY 1,2;
