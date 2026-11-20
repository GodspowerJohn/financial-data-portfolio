# Financial Performance & Cash Flow Forecasting

 **Portfolio demonstration using fully synthetic data. No employer, customer or bank records.**

 ## Business question
 How can finance teams anticipate liquidity changes and evaluate downside exposure before planning commitments?

 ## Project workflow
 1. Create 36 synthetic months of revenue, costs, EBITDA, capex and working-capital movements.
2. Fit a trend-and-seasonality regression on the first 30 months.
3. Evaluate a six-month holdout, then forecast six future months.
4. Apply explicit downside/base/upside revenue multipliers to build cash scenarios.

 ## Reproduce
 From the repository root:
 ```bash
 pip install -r projects/requirements.txt
 python projects/cashflow-forecast/src/run.py
 ```
 This script overwrites `projects/cashflow-forecast/data/*.csv` and `results/metrics.json` deterministically with a fixed random seed. Use Python 3.10+.

 ## Main files
 - `src/run.py`: deterministic generation and analysis, with evaluation or scenario logic
 - `src/analysis.sql`: PostgreSQL 14+ exploratory queries
 - `powerbi/measures.dax`: Power BI measures with named tables
 - `powerbi/REPORT_SPEC.md`: report pages, data model and QA checklist
 - `data/monthly_financials.csv`: synthetic outputs (additional files as applicable)
 - `results/metrics.json`: reproducible metrics for the accompanying case study

 ## Analytical interpretation
 - Backtest error indicates how closely the simple model matched holdout revenue.
- Cash scenarios reveal the sensitivity of ending liquidity to revenue assumptions.
- Scenario outputs are not probability-weighted forecasts.

 ## Recommended business actions
 - Build a rolling 13-week cash monitoring view for short-term management.
- Reconcile forecast assumptions with contracts and actual receivables.
- Add variable-cost and working-capital scenario sensitivity.

 ## Limitations
 The financial series is synthetic; the model assumes stable seasonality, expense relationships and cash timing. Forecasts do not apply to a real company.

 ## Reproducibility
 All figures on the web case study should be read as values from this artificial demonstration, not professional achievements or business facts. Verify the metrics by rerunning the script and comparing `results/metrics.json`. In Power BI Desktop, import CSVs and create the measures documented under `powerbi/`.
