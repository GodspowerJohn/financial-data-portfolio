"""Synthetic process-flow and service-level bottleneck analysis.
Run: python projects/process-efficiency/src/run.py
"""
from pathlib import Path
import numpy as np,pandas as pd,json
BASE=Path(__file__).resolve().parents[1];rng=np.random.default_rng(84107)
n=2250
team=['Manual Deposit','Payout Review','Commission Adjustment','Customer Resolution']
workflow=rng.choice(team,n,p=[.39,.30,.16,.15])
created=pd.Timestamp('2026-08-01')+pd.to_timedelta(np.sort(rng.integers(0,90*24*60,n)),unit='m')
priority=rng.choice(['Normal','High'],n,p=[.82,.18]);queue=[];service=[];rework=[];sla=[]
for i in range(n):
 w=workflow[i];limit={'Manual Deposit':5,'Payout Review':15,'Commission Adjustment':30,'Customer Resolution':45}[w]
 q=float(rng.gamma(2.3,{'Manual Deposit':1.4,'Payout Review':3.6,'Commission Adjustment':7.4,'Customer Resolution':12}[w]))
 if priority[i]=='High':q*=.65
 s=float(rng.gamma(2,{'Manual Deposit':.95,'Payout Review':2.4,'Commission Adjustment':4.0,'Customer Resolution':6.5}[w]))
 rw=int(rng.binomial(1,{'Manual Deposit':.045,'Payout Review':.08,'Commission Adjustment':.17,'Customer Resolution':.15}[w]))
 if rw:s+=float(rng.uniform(4,23))
 queue.append(round(q,2));service.append(round(s,2));rework.append(rw);sla.append(limit)
df=pd.DataFrame({'case_id':[f'CASE-{i+1:06d}' for i in range(n)],'created_at':created.astype(str),'workflow':workflow,'priority':priority,'queue_minutes':queue,'processing_minutes':service,'rework':rework,'sla_target_minutes':sla})
df['elapsed_minutes']=(df.queue_minutes+df.processing_minutes).round(2)
df['within_sla']=df.elapsed_minutes<=df.sla_target_minutes
# Counterfactual queue reduction is a what-if, NOT a measured outcome.
df['whatif_elapsed_minutes']=.8*df.queue_minutes+df.processing_minutes
df['whatif_within_sla']=df.whatif_elapsed_minutes<=df.sla_target_minutes
(BASE/'data').mkdir(exist_ok=True);(BASE/'results').mkdir(exist_ok=True)
df.to_csv(BASE/'data'/'process_cases.csv',index=False)
by=df.groupby('workflow').agg(cases=('case_id','count'),sla_rate=('within_sla','mean'),average_queue_minutes=('queue_minutes','mean'),rework_rate=('rework','mean')).round(4)
metrics={'case_count':n,'overall_sla_rate':round(float(df.within_sla.mean()),4),
'average_queue_minutes':round(float(df.queue_minutes.mean()),2),
'average_handle_minutes':round(float(df.processing_minutes.mean()),2),
'overall_rework_rate':round(float(df.rework.mean()),4),
'workflow_results':by.to_dict(orient='index'),
'whatif_queue_reduction':.20,
'whatif_sla_rate':round(float(df.whatif_within_sla.mean()),4),
'whatif_improvement_pp':round(float((df.whatif_within_sla.mean()-df.within_sla.mean())*100),2),
'queue_time_saved_hours':round(float(.2*df.queue_minutes.sum()/60),2)}
(BASE/'results'/'metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
