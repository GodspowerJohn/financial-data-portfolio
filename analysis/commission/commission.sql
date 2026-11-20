-- PostgreSQL: after importing data/synthetic_agent_commissions.csv into synthetic_agent_commissions
-- 40% is an illustrative analytical threshold, not an employer policy.
WITH agent_economics AS (
 SELECT month, agent_id, product, stake_ngn, ggr_ngn, total_commission_ngn,
  CASE WHEN ggr_ngn > 0 THEN total_commission_ngn / NULLIF(ggr_ngn, 0) ELSE NULL END AS commission_ggr_ratio,
  ggr_ngn - total_commission_ngn AS contribution_ngn
 FROM synthetic_agent_commissions
)
SELECT month, product,
 COUNT(*) AS records,
 ROUND(SUM(stake_ngn)::numeric,2) AS total_stake_ngn,
 ROUND(SUM(ggr_ngn)::numeric,2) AS ggr_ngn,
 ROUND(SUM(total_commission_ngn)::numeric,2) AS commission_ngn,
 ROUND((100*SUM(total_commission_ngn)/NULLIF(SUM(ggr_ngn),0))::numeric,2) AS aggregate_commission_pct,
 COUNT(*) FILTER (WHERE ggr_ngn <= 0 OR commission_ggr_ratio > .40) AS rows_for_review
FROM agent_economics
GROUP BY month, product
ORDER BY month, product;
