# Reproducible analytical findings | Agent Commission Profitability & Cost Optimisation

 **Evidence base:** Synthetic project dataset generated from a fixed random seed and analysed with `src/run.py`.

 ## Findings
 1. Loss-making agent-months are measurable even when aggregate GGR is positive.
2. A strict profit-linked cap lowers payouts in low-margin periods.
3. Estimated savings are scenario arithmetic, not evidence of a real operational outcome.

 ## Actions to test
 1. Stress-test payout fairness and minimum agent economics.
2. Use hold-margin bands and exception approval in policy design.
3. Pilot policy changes and monitor subsequent volume and retention.

 ## Interpretation and risks
 Commission rules are invented for demonstration and are not any employer’s actual rules. Reduced payout does not automatically imply higher long-term profit because behaviour may change.

 ## Metrics
 ```json
 {
  "agent_month_records": 720,
  "unique_agents": 80,
  "months": 9,
  "stake_ngn": 1014228384.49,
  "ggr_ngn": 102870843.67,
  "positive_ggr_ngn": 115712960.71,
  "baseline_commission_ngn": 57050190.71,
  "scenario_commission_ngn": 32012516.35,
  "scenario_reduction_ngn": 25037674.36,
  "baseline_ratio_positive_ggr": 0.493,
  "scenario_ratio_positive_ggr": 0.2767,
  "baseline_loss_making_agent_months": 240,
  "scenario_loss_making_agent_months": 135,
  "product_summary": {
    "Sportsbook": {
      "ggr_ngn": 49846806,
      "baseline_commission_ngn": 29555843,
      "scenario_commission_ngn": 15934903
    },
    "Virtual A": {
      "ggr_ngn": 29948140,
      "baseline_commission_ngn": 15929650,
      "scenario_commission_ngn": 9274950
    },
    "Virtual B": {
      "ggr_ngn": 23075897,
      "baseline_commission_ngn": 11564698,
      "scenario_commission_ngn": 6802663
    }
  }
}
 ```
