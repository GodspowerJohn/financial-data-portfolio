# Financial Fraud Detection & Risk Intelligence

 **Portfolio demonstration using fully synthetic data. No employer, customer or bank records.**

 ## Business question
 How can investigators prioritise suspicious activity without overwhelming the queue with false alerts?

 ## Project workflow
 1. Generate 4,800 labelled synthetic transactions with time, amount, velocity, device and cross-border indicators.
2. Use a 60/20/20 chronological split; fit a class-weighted logistic regression.
3. Choose the alert threshold on validation records only, then evaluate untouched test transactions.
4. Compare the model with a simple review rule, including false alerts and missed risk.

 ## Reproduce
 From the repository root:
 ```bash
 pip install -r projects/requirements.txt
 python projects/fraud-intelligence/src/run.py
 ```
 This script overwrites `projects/fraud-intelligence/data/*.csv` and `results/metrics.json` deterministically with a fixed random seed. Use Python 3.10+.

 ## Main files
 - `src/run.py`: deterministic generation and analysis, with evaluation or scenario logic
 - `src/analysis.sql`: PostgreSQL 14+ exploratory queries
 - `powerbi/measures.dax`: Power BI measures with named tables
 - `powerbi/REPORT_SPEC.md`: report pages, data model and QA checklist
 - `data/transactions.csv`: synthetic outputs (additional files as applicable)
 - `results/metrics.json`: reproducible metrics for the accompanying case study

 ## Analytical interpretation
 - Precision and recall are reported from the held-out period, not training accuracy.
- The dataset is imbalanced; a confident model can still generate costly false alerts.
- A risk score supports analyst triage but is not proof of wrongdoing.

 ## Recommended business actions
 - Route high-scoring cases to an investigator queue.
- Track false-positive rate and missed fraud as competing objectives.
- Audit drift, fairness, and alert capacity before a real deployment.

 ## Limitations
 All labels and features are simulated. The pattern is engineered and cannot establish actual fraud detection capability. No sensitive identifiers are present.

 ## Reproducibility
 All figures on the web case study should be read as values from this artificial demonstration, not professional achievements or business facts. Verify the metrics by rerunning the script and comparing `results/metrics.json`. In Power BI Desktop, import CSVs and create the measures documented under `powerbi/`.
