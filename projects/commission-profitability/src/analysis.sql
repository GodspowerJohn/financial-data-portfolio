-- PostgreSQL 14+. Synthetic incentive economics only.
CREATE TABLE IF NOT EXISTS agent_months (
 month TEXT,agent_id TEXT,product TEXT,stake_ngn NUMERIC(16,2),betslips INT,
 ggr_ngn NUMERIC(16,2),weekly_example_ngn NUMERIC(16,2),
 baseline_commission_ngn NUMERIC(16,2),scenario_commission_ngn NUMERIC(16,2),
 baseline_after_commission_ngn NUMERIC(16,2),scenario_after_commission_ngn NUMERIC(16,2),
 PRIMARY KEY(month,agent_id)
);
-- Load using psql: \copy agent_months FROM 'data/agent_months.csv' CSV HEADER
SELECT month,SUM(ggr_ngn) AS ggr,
 SUM(baseline_commission_ngn) AS baseline_payout,
 SUM(scenario_commission_ngn) AS scenario_payout,
 SUM(baseline_commission_ngn-scenario_commission_ngn) AS scenario_savings
FROM agent_months GROUP BY month ORDER BY month;
SELECT product,COUNT(*) AS agent_months,
 SUM(CASE WHEN baseline_after_commission_ngn<0 THEN 1 ELSE 0 END) AS baseline_negative_margin,
 SUM(CASE WHEN scenario_after_commission_ngn<0 THEN 1 ELSE 0 END) AS scenario_negative_margin,
 ROUND(SUM(scenario_commission_ngn)/NULLIF(SUM(GREATEST(ggr_ngn,0)),0)*100,2) AS scenario_pct_positive_ggr
FROM agent_months GROUP BY product ORDER BY scenario_pct_positive_ggr DESC;
