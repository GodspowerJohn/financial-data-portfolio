# Reproducible analytical findings | Financial Performance & Cash Flow Forecasting

 **Evidence base:** Synthetic project dataset generated from a fixed random seed and analysed with `src/run.py`.

 ## Findings
 1. Backtest error indicates how closely the simple model matched holdout revenue.
2. Cash scenarios reveal the sensitivity of ending liquidity to revenue assumptions.
3. Scenario outputs are not probability-weighted forecasts.

 ## Actions to test
 1. Build a rolling 13-week cash monitoring view for short-term management.
2. Reconcile forecast assumptions with contracts and actual receivables.
3. Add variable-cost and working-capital scenario sensitivity.

 ## Interpretation and risks
 The financial series is synthetic; the model assumes stable seasonality, expense relationships and cash timing. Forecasts do not apply to a real company.

 ## Metrics
 ```json
 {
  "history_months": 36,
  "backtest_months": 6,
  "revenue_mae_ngn": 764901.62,
  "latest_month_revenue_ngn": 38597248.13,
  "latest_month_ebitda_ngn": 10963474.94,
  "latest_cash_ngn": 322161650.59,
  "historical_ebitda_margin": 0.2985,
  "next_six_months_revenue_by_scenario_ngn": {
    "Base": 261806438.15,
    "Downside": 230389665.57,
    "Upside": 293223210.73
  },
  "forecast_cash_at_six_months_ngn": {
    "Downside": 382924855.9,
    "Base": 401274996.01,
    "Upside": 419625136.11
  },
  "assumptions": {
    "downside_revenue_multiplier": 0.88,
    "upside_revenue_multiplier": 1.12,
    "variable_cost_ratio": 0.4159
  }
}
 ```
