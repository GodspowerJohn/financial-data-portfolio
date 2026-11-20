# Reproducible analytical findings | Business Process Efficiency & Operational Performance

 **Evidence base:** Synthetic project dataset generated from a fixed random seed and analysed with `src/run.py`.

 ## Findings
 1. SLA performance differs substantially across workflows.
2. Queue delay and rework are different bottlenecks requiring different interventions.
3. The what-if improvement depends entirely on the assumed reduction being achievable.

 ## Actions to test
 1. Map each workflow and document hand-offs and owners.
2. Instrument timestamps for each approval stage.
3. Test queue-triage and staffing changes using a controlled pilot.

 ## Interpretation and risks
 All cases, delays and SLA targets are synthetic; the 20% queue improvement is a hypothetical scenario, not a measured process change.

 ## Metrics
 ```json
 {
  "case_count": 2250,
  "overall_sla_rate": 0.616,
  "average_queue_minutes": 10.03,
  "average_handle_minutes": 6.7,
  "overall_rework_rate": 0.0893,
  "workflow_results": {
    "Commission Adjustment": {
      "cases": 350,
      "sla_rate": 0.6829,
      "average_queue_minutes": 15.7511,
      "rework_rate": 0.1657
    },
    "Customer Resolution": {
      "cases": 347,
      "sla_rate": 0.6427,
      "average_queue_minutes": 25.6483,
      "rework_rate": 0.1585
    },
    "Manual Deposit": {
      "cases": 848,
      "sla_rate": 0.5389,
      "average_queue_minutes": 3.1692,
      "rework_rate": 0.0483
    },
    "Payout Review": {
      "cases": 705,
      "sla_rate": 0.6624,
      "average_queue_minutes": 7.7586,
      "rework_rate": 0.0667
    }
  },
  "whatif_queue_reduction": 0.2,
  "whatif_sla_rate": 0.6982,
  "whatif_improvement_pp": 8.22,
  "queue_time_saved_hours": 75.23
}
 ```
