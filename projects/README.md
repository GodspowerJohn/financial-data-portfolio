# Five reproducible analytics projects

This directory contains five **fully synthetic** case studies. Each includes runnable Python, PostgreSQL queries, CSV datasets, machine-readable result metrics, a published HTML case study and Power BI measure specifications.

## Projects
1. Fraud Detection & Risk Intelligence: `fraud-intelligence/`
2. Commission Profitability Optimisation: `commission-profitability/`
3. Financial & Cash Flow Forecasting: `cashflow-forecast/`
4. Automated Payment Reconciliation: `payment-reconciliation/`
5. Business Process Efficiency: `process-efficiency/`

## Run locally
```bash
python -m pip install -r projects/requirements.txt
python projects/fraud-intelligence/src/run.py
python projects/commission-profitability/src/run.py
python projects/cashflow-forecast/src/run.py
python projects/payment-reconciliation/src/run.py
python projects/process-efficiency/src/run.py
```

These commands regenerate the synthetic data and JSON statistics using fixed random seeds. No private data are used. Use Python 3.10+.

**Power BI**: the case studies contain importable CSV, DAX and report specifications. They do not contain a compiled `.pbix` file. Published website charts are SVG visualisations made from the synthetic data.

**Integrity**: the results are illustrative, not claims of real-world project performance, audited outcomes or confirmed fraud cases. Never use synthetic model scores to make decisions about real people.
