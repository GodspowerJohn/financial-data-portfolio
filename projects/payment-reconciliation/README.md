# Automated Payment Reconciliation & Exception Management

 **Portfolio demonstration using fully synthetic data. No employer, customer or bank records.**

 ## Business question
 How can finance operations systematically detect missing settlements, duplicate credits, amount mismatches and delayed bank postings?

 ## Project workflow
 1. Generate distinct provider transaction records and bank credit entries with stable synthetic references.
2. Join references and aggregate bank records to identify duplicate entries.
3. Apply a clear exception-priority rule: missing, duplicate, amount mismatch, delayed, then matched.
4. Quantify missing expected value and absolute settlement variance.

 ## Reproduce
 From the repository root:
 ```bash
 pip install -r projects/requirements.txt
 python projects/payment-reconciliation/src/run.py
 ```
 This script overwrites `projects/payment-reconciliation/data/*.csv` and `results/metrics.json` deterministically with a fixed random seed. Use Python 3.10+.

 ## Main files
 - `src/run.py`: deterministic generation and analysis, with evaluation or scenario logic
 - `src/analysis.sql`: PostgreSQL 14+ exploratory queries
 - `powerbi/measures.dax`: Power BI measures with named tables
 - `powerbi/REPORT_SPEC.md`: report pages, data model and QA checklist
 - `data/reconciliation_output.csv`: synthetic outputs (additional files as applicable)
 - `results/metrics.json`: reproducible metrics for the accompanying case study

 ## Analytical interpretation
 - A successful payment status does not guarantee a matching bank credit.
- Absolute variance and missing expected value measure different exposures.
- Duplicate credits require separate investigation from delayed payments.

 ## Recommended business actions
 - Queue exceptions by age, value and provider.
- Preserve immutable source exports and daily cutoff times.
- Create owner, response SLA and resolution audit fields before production use.

 ## Limitations
 These are synthetic events with reference-level matches only. Real settlement batches may require many-to-many matching and fee-calendar rules.

 ## Reproducibility
 All figures on the web case study should be read as values from this artificial demonstration, not professional achievements or business facts. Verify the metrics by rerunning the script and comparing `results/metrics.json`. In Power BI Desktop, import CSVs and create the measures documented under `powerbi/`.
