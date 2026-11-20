-- PostgreSQL 14+. Historical and scenario records are independently simulated.
CREATE TABLE IF NOT EXISTS monthly_financials (
 month TEXT PRIMARY KEY,revenue_ngn NUMERIC(16,2),variable_cost_ngn NUMERIC(16,2),
 fixed_cost_ngn NUMERIC(16,2),ebitda_ngn NUMERIC(16,2),
 capex_ngn NUMERIC(16,2),working_capital_increase_ngn NUMERIC(16,2),
 net_cashflow_ngn NUMERIC(16,2),ending_cash_ngn NUMERIC(16,2)
);
CREATE TABLE IF NOT EXISTS forecast_scenarios (
 month TEXT,scenario TEXT,forecast_revenue_ngn NUMERIC(16,2),
 forecast_ebitda_ngn NUMERIC(16,2),forecast_net_cashflow_ngn NUMERIC(16,2),
 forecast_ending_cash_ngn NUMERIC(16,2),PRIMARY KEY(month,scenario)
);
-- Load CSVs with psql \copy after creating tables.
SELECT LEFT(month,4) AS year,ROUND(SUM(revenue_ngn),2) AS revenue_ngn,
 ROUND(SUM(ebitda_ngn),2) AS ebitda_ngn,
 ROUND(100*SUM(ebitda_ngn)/NULLIF(SUM(revenue_ngn),0),2) AS margin_pct
FROM monthly_financials GROUP BY 1 ORDER BY 1;
SELECT scenario,SUM(forecast_revenue_ngn) AS forecast_6m_revenue,
 (ARRAY_AGG(forecast_ending_cash_ngn ORDER BY month DESC))[1] AS month6_cash
FROM forecast_scenarios GROUP BY scenario ORDER BY scenario;
