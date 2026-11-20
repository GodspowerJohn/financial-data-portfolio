"""Synthetic agent economics: compare status quo with profit-sensitive commission cap.
Run: python projects/commission-profitability/src/run.py
Illustrative rules are NOT an existing organisation's commission policy.
"""
from pathlib import Path
import numpy as np,pandas as pd,json
BASE=Path(__file__).resolve().parents[1];rng=np.random.default_rng(9061)
rows=[]
for month in pd.period_range('2026-01','2026-09',freq='M'):
 for agent in range(1,81):
  product=rng.choice(['Sportsbook','Virtual A','Virtual B'],p=[.55,.27,.18]);stake=float(rng.uniform(150_000,2_600_000));bets=int(rng.integers(70,2500))
  margin=float(np.clip(rng.normal(.105,.115),-.25,.42));ggr=round(stake*margin,2)
  # Existing illustrative structure: 5% of stake for qualified agents, with month-end top-up to 30% of positive GGR.
  weekly=round(.05*stake if stake>=100000 and bets>=100 else 0,2)
  baseline=round(max(weekly,.30*max(ggr,0)),2)
  # Scenario: lower stake component; no more than 40% of positive GGR (zero in loss months).
  tier=.01 if stake>=1_000_000 and bets>=800 else 0
  scenario_raw=max((.03+tier)*stake if bets>=100 else 0,.25*max(ggr,0))
  scenario=round(min(scenario_raw,.40*max(ggr,0)),2)
  rows.append([str(month),f'AGT-{agent:04d}',product,round(stake,2),bets,ggr,weekly,baseline,scenario])
df=pd.DataFrame(rows,columns=['month','agent_id','product','stake_ngn','betslips','ggr_ngn','weekly_example_ngn','baseline_commission_ngn','scenario_commission_ngn'])
df['baseline_after_commission_ngn']=df.ggr_ngn-df.baseline_commission_ngn
df['scenario_after_commission_ngn']=df.ggr_ngn-df.scenario_commission_ngn
(BASE/'data').mkdir(exist_ok=True);(BASE/'results').mkdir(exist_ok=True)
df.to_csv(BASE/'data'/'agent_months.csv',index=False)
positive_ggr=float(df.ggr_ngn.clip(lower=0).sum());baseline=float(df.baseline_commission_ngn.sum());scenario=float(df.scenario_commission_ngn.sum())
metrics={'agent_month_records':len(df),'unique_agents':df.agent_id.nunique(),'months':df.month.nunique(),
'stake_ngn':round(float(df.stake_ngn.sum()),2),'ggr_ngn':round(float(df.ggr_ngn.sum()),2),
'positive_ggr_ngn':round(positive_ggr,2),'baseline_commission_ngn':round(baseline,2),
'scenario_commission_ngn':round(scenario,2),'scenario_reduction_ngn':round(baseline-scenario,2),
'baseline_ratio_positive_ggr':round(baseline/positive_ggr,4),'scenario_ratio_positive_ggr':round(scenario/positive_ggr,4),
'baseline_loss_making_agent_months':int((df.baseline_after_commission_ngn<0).sum()),
'scenario_loss_making_agent_months':int((df.scenario_after_commission_ngn<0).sum()),
'product_summary':df.groupby('product')[['ggr_ngn','baseline_commission_ngn','scenario_commission_ngn']].sum().round().astype(int).to_dict(orient='index')}
(BASE/'results'/'metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
