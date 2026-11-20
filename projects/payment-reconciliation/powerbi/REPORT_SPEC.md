# Power BI dashboard implementation | Automated Payment Reconciliation & Exception Management

This repository includes data and DAX measure definitions, **not a compiled `.pbix` report**.

1. In Power BI Desktop, Get Data → Text/CSV and import every CSV in `data/`.
2. Rename tables to match `powerbi/measures.dax` (e.g., `FraudTransactions`, `AgentMonths`, `Financials`, `ForecastScenarios`, `ReconciliationOutput`, `ProcessCases`).
3. Convert date/time columns to Date/DateTime. Convert currency fields to decimal number, identity fields to text, boolean columns to True/False.
4. Paste the measures one by one as new measures.
5. Create an overview page with headline metrics and a slicer for month, workflow or provider, as appropriate.
6. Add a diagnostic page by key segment, an exception or model-evaluation page, and an assumptions page.
7. QA: cross-check total rows, distinct IDs, currency measures and percentages against `results/metrics.json`; verify each slicer.
8. Export anonymised screenshots only. Do not publish any private data through Power BI Publish to web.

### Suggested report pages
- Executive overview: key results and movement through time
- Segment drill-down: transaction type/provider/product/workflow or scenario
- Exceptions and controls: outliers, failures, status and risk owners
- Methods, definitions and limitations: metric dictionary and scenario caveats

### Accuracy warning
The chart figures are generated from a synthetic experiment and are not real operational statistics. The submitted website contains rendered SVG visualisations; a native editable Power BI PBIX still needs to be constructed with Desktop.
