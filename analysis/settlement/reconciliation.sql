-- PostgreSQL: after importing data/synthetic_settlements.csv into synthetic_settlements
-- Missing bank settlements represent 100% of expected value at risk.
WITH checks AS (
  SELECT provider, month, reconciliation_status,
    expected_settlement_ngn,
    COALESCE(bank_settlement_ngn, 0) AS received_ngn,
    settlement_delay_hours,
    ABS(expected_settlement_ngn - COALESCE(bank_settlement_ngn, 0)) AS absolute_exposure_ngn
  FROM synthetic_settlements
)
SELECT month, provider,
  COUNT(*) AS transaction_count,
  COUNT(*) FILTER (WHERE reconciliation_status = 'Matched') AS matched_transactions,
  ROUND(100.0 * COUNT(*) FILTER (WHERE reconciliation_status = 'Matched') / NULLIF(COUNT(*),0),2) AS match_rate_pct,
  ROUND(SUM(absolute_exposure_ngn)::numeric,2) AS unreconciled_exposure_ngn,
  COUNT(*) FILTER (WHERE settlement_delay_hours > 48) AS over_48_hours
FROM checks
GROUP BY month,provider
ORDER BY month,provider;
