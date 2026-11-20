# Reproducible analytical findings | Automated Payment Reconciliation & Exception Management

 **Evidence base:** Synthetic project dataset generated from a fixed random seed and analysed with `src/run.py`.

 ## Findings
 1. A successful payment status does not guarantee a matching bank credit.
2. Absolute variance and missing expected value measure different exposures.
3. Duplicate credits require separate investigation from delayed payments.

 ## Actions to test
 1. Queue exceptions by age, value and provider.
2. Preserve immutable source exports and daily cutoff times.
3. Create owner, response SLA and resolution audit fields before production use.

 ## Interpretation and risks
 These are synthetic events with reference-level matches only. Real settlement batches may require many-to-many matching and fee-calendar rules.

 ## Metrics
 ```json
 {
  "provider_transactions": 2100,
  "bank_credit_entries": 2063,
  "matched_transactions": 1785,
  "exception_transactions": 315,
  "match_rate": 0.85,
  "exception_counts": {
    "Matched": 1785,
    "Missing": 90,
    "Amount mismatch": 89,
    "Delayed": 83,
    "Duplicate": 53
  },
  "expected_net_ngn": 471170176.86,
  "bank_credits_ngn": 462349350.84,
  "absolute_unreconciled_variance_ngn": 32816526.04,
  "unmatched_expected_ngn": 20787155.76
}
 ```
