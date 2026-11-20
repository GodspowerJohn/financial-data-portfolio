# Business Process Efficiency & Operational Performance

 **Portfolio demonstration using fully synthetic data. No employer, customer or bank records.**

 ## Business question
 Which operational workflows miss service targets, and where could reducing queue time create measurable improvements?

 ## Project workflow
 1. Simulate 2,250 cases across manual deposits, payout reviews, commission adjustments and customer resolution.
2. Separate waiting/queue time from active handling time and rework.
3. Compare SLA attainment, average queue and rework by workflow.
4. Model a hypothetical 20% queue-time reduction without claiming real-world impact.

 ## Reproduce
 From the repository root:
 ```bash
 pip install -r projects/requirements.txt
 python projects/process-efficiency/src/run.py
 ```
 This script overwrites `projects/process-efficiency/data/*.csv` and `results/metrics.json` deterministically with a fixed random seed. Use Python 3.10+.

 ## Main files
 - `src/run.py`: deterministic generation and analysis, with evaluation or scenario logic
 - `src/analysis.sql`: PostgreSQL 14+ exploratory queries
 - `powerbi/measures.dax`: Power BI measures with named tables
 - `powerbi/REPORT_SPEC.md`: report pages, data model and QA checklist
 - `data/process_cases.csv`: synthetic outputs (additional files as applicable)
 - `results/metrics.json`: reproducible metrics for the accompanying case study

 ## Analytical interpretation
 - SLA performance differs substantially across workflows.
- Queue delay and rework are different bottlenecks requiring different interventions.
- The what-if improvement depends entirely on the assumed reduction being achievable.

 ## Recommended business actions
 - Map each workflow and document hand-offs and owners.
- Instrument timestamps for each approval stage.
- Test queue-triage and staffing changes using a controlled pilot.

 ## Limitations
 All cases, delays and SLA targets are synthetic; the 20% queue improvement is a hypothetical scenario, not a measured process change.

 ## Reproducibility
 All figures on the web case study should be read as values from this artificial demonstration, not professional achievements or business facts. Verify the metrics by rerunning the script and comparing `results/metrics.json`. In Power BI Desktop, import CSVs and create the measures documented under `powerbi/`.
