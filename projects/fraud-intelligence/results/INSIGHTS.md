# Reproducible analytical findings | Financial Fraud Detection & Risk Intelligence

 **Evidence base:** Synthetic project dataset generated from a fixed random seed and analysed with `src/run.py`.

 ## Findings
 1. Precision and recall are reported from the held-out period, not training accuracy.
2. The dataset is imbalanced; a confident model can still generate costly false alerts.
3. A risk score supports analyst triage but is not proof of wrongdoing.

 ## Actions to test
 1. Route high-scoring cases to an investigator queue.
2. Track false-positive rate and missed fraud as competing objectives.
3. Audit drift, fairness, and alert capacity before a real deployment.

 ## Interpretation and risks
 All labels and features are simulated. The pattern is engineered and cannot establish actual fraud detection capability. No sensitive identifiers are present.

 ## Metrics
 ```json
 {
  "sample_transactions": 4800,
  "fraud_cases": 119,
  "fraud_rate": 0.0248,
  "train_rows": 2880,
  "validation_rows": 960,
  "test_rows": 960,
  "threshold": 0.875,
  "precision": 0.2593,
  "recall": 0.3889,
  "f1": 0.3111,
  "average_precision": 0.2913,
  "tp": 7,
  "fp": 20,
  "tn": 922,
  "fn": 11,
  "test_fraud_cases": 18,
  "test_flagged": 27,
  "rule_precision": 0.6,
  "rule_recall": 0.1667,
  "false_positive_rate": 0.0212,
  "review_amount_ngn": 8319932.61,
  "missed_fraud_amount_ngn": 1154468.76
}
 ```
