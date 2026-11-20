-- PostgreSQL 14+. Synthetic case-level process times.
CREATE TABLE IF NOT EXISTS process_cases (
 case_id TEXT PRIMARY KEY,created_at TIMESTAMP,workflow TEXT,priority TEXT,
 queue_minutes NUMERIC(10,2),processing_minutes NUMERIC(10,2),rework INT,
 sla_target_minutes INT,elapsed_minutes NUMERIC(10,2),within_sla BOOLEAN,
 whatif_elapsed_minutes NUMERIC(10,2),whatif_within_sla BOOLEAN
);
-- Load using psql: \copy process_cases FROM 'data/process_cases.csv' CSV HEADER
SELECT workflow,COUNT(*) AS cases,
 ROUND(AVG(CASE WHEN within_sla THEN 1.0 ELSE 0.0 END)*100,2) AS sla_rate_pct,
 ROUND(AVG(queue_minutes),2) AS avg_queue_minutes,
 ROUND(AVG(CASE WHEN rework=1 THEN 1.0 ELSE 0.0 END)*100,2) AS rework_rate_pct,
 ROUND(PERCENTILE_CONT(.90) WITHIN GROUP (ORDER BY elapsed_minutes)::numeric,2) AS p90_total_minutes
FROM process_cases GROUP BY workflow ORDER BY sla_rate_pct ASC;
SELECT ROUND(AVG(CASE WHEN within_sla THEN 1.0 ELSE 0.0 END)*100,2) AS baseline_sla_pct,
 ROUND(AVG(CASE WHEN whatif_within_sla THEN 1.0 ELSE 0.0 END)*100,2) AS simulated_sla_pct
FROM process_cases;
