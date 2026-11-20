# Agent Commission Profitability & Cost Optimisation

 **Portfolio demonstration using fully synthetic data. No employer, customer or bank records.**

 ## Business question
 Which illustrative commission structure better protects contribution margin without ignoring incentive trade-offs?

 ## Project workflow
 1. Simulate 80 agents across nine months and several product categories.
2. Compare a qualifying 5% stake-linked payout and 30% positive-GGR monthly floor against a smaller stake component and a 40% positive-GGR payout ceiling.
3. Calculate payout cost, loss-making agent-months and product-level differences.
4. Explain how guardrails can reduce costs but also change agent incentives.

 ## Reproduce
 From the repository root:
 ```bash
 pip install -r projects/requirements.txt
 python projects/commission-profitability/src/run.py
 ```
 This script overwrites `projects/commission-profitability/data/*.csv` and `results/metrics.json` deterministically with a fixed random seed. Use Python 3.10+.

 ## Main files
 - `src/run.py`: deterministic generation and analysis, with evaluation or scenario logic
 - `src/analysis.sql`: PostgreSQL 14+ exploratory queries
 - `powerbi/measures.dax`: Power BI measures with named tables
 - `powerbi/REPORT_SPEC.md`: report pages, data model and QA checklist
 - `data/agent_months.csv`: synthetic outputs (additional files as applicable)
 - `results/metrics.json`: reproducible metrics for the accompanying case study

 ## Analytical interpretation
 - Loss-making agent-months are measurable even when aggregate GGR is positive.
- A strict profit-linked cap lowers payouts in low-margin periods.
- Estimated savings are scenario arithmetic, not evidence of a real operational outcome.

 ## Recommended business actions
 - Stress-test payout fairness and minimum agent economics.
- Use hold-margin bands and exception approval in policy design.
- Pilot policy changes and monitor subsequent volume and retention.

 ## Limitations
 Commission rules are invented for demonstration and are not any employer’s actual rules. Reduced payout does not automatically imply higher long-term profit because behaviour may change.

 ## Reproducibility
 All figures on the web case study should be read as values from this artificial demonstration, not professional achievements or business facts. Verify the metrics by rerunning the script and comparing `results/metrics.json`. In Power BI Desktop, import CSVs and create the measures documented under `powerbi/`.
