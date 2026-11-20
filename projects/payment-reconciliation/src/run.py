"""Reconcile synthetic provider transactions and synthetic bank credits by stable IDs.
Run: python projects/payment-reconciliation/src/run.py
"""
from pathlib import Path
import numpy as np,pandas as pd,json
BASE=Path(__file__).resolve().parents[1];rng=np.random.default_rng(42422)
n=2100;providers=['Paystack','Monnify','Interswitch','Flutterwave']
created=pd.Timestamp('2026-07-01')+pd.to_timedelta(np.sort(rng.integers(0,65*24*60,n)),unit='m')
provider=rng.choice(providers,n)
amount=np.round(rng.uniform(1500,460000,n),2)
fee=np.round(np.minimum(amount*.012,2000),2)
expected=np.round(amount-fee,2)
state=rng.choice(['Matched','Missing','Amount mismatch','Duplicate','Delayed'],n,p=[.855,.045,.035,.025,.04])
source=pd.DataFrame({'reference':[f'PAY-{i+1:06d}' for i in range(n)],'payment_time':created.astype(str),'provider':provider,'gross_ngn':amount,'fee_ngn':fee,'expected_net_ngn':expected})
rows=[]
for i in range(n):
 if state[i]=='Missing':continue
 value=expected[i]
 if state[i]=='Amount mismatch': value=round(max(0,value+float(rng.choice([-1,1]))*rng.uniform(100,1500)),2)
 lag=int(rng.integers(3,90) if state[i]!='Delayed' else rng.integers(1500,4800))
 posted=created[i]+pd.Timedelta(minutes=lag)
 rows.append([f'BK-{len(rows)+1:07d}',source.reference.iloc[i],str(posted),float(value)])
 if state[i]=='Duplicate':rows.append([f'BK-{len(rows)+1:07d}',source.reference.iloc[i],str(posted+pd.Timedelta(minutes=3)),float(value)])
bank=pd.DataFrame(rows,columns=['bank_entry_id','reference','posted_at','credit_ngn'])
(BASE/'data').mkdir(exist_ok=True);(BASE/'results').mkdir(exist_ok=True)
source.to_csv(BASE/'data'/'provider_transactions.csv',index=False)
bank.to_csv(BASE/'data'/'bank_credits.csv',index=False)
agg=bank.groupby('reference').agg(bank_entries=('credit_ngn','size'),bank_total_ngn=('credit_ngn','sum'),first_posted=('posted_at','min')).reset_index()
merged=source.merge(agg,on='reference',how='left')
merged.bank_entries=merged.bank_entries.fillna(0).astype(int);merged.bank_total_ngn=merged.bank_total_ngn.fillna(0)
merged['delay_hours']=(pd.to_datetime(merged.first_posted)-pd.to_datetime(merged.payment_time)).dt.total_seconds()/3600
merged['variance_ngn']=np.round(merged.bank_total_ngn-merged.expected_net_ngn,2)
merged['recon_status']=np.select([merged.bank_entries.eq(0),merged.bank_entries.gt(1),merged.variance_ngn.abs().gt(.01),merged.delay_hours.gt(24)],['Missing','Duplicate','Amount mismatch','Delayed'],default='Matched')
merged.to_csv(BASE/'data'/'reconciliation_output.csv',index=False)
counts={str(k):int(v) for k,v in merged.recon_status.value_counts().items()}
metrics={'provider_transactions':n,'bank_credit_entries':len(bank),'matched_transactions':counts.get('Matched',0),
'exception_transactions':int(n-counts.get('Matched',0)),'match_rate':round(counts.get('Matched',0)/n,4),
'exception_counts':counts,'expected_net_ngn':round(float(source.expected_net_ngn.sum()),2),
'bank_credits_ngn':round(float(bank.credit_ngn.sum()),2),
'absolute_unreconciled_variance_ngn':round(float(merged.loc[merged.recon_status!='Matched','variance_ngn'].abs().sum()),2),
'unmatched_expected_ngn':round(float(merged.loc[merged.recon_status=='Missing','expected_net_ngn'].sum()),2)}
(BASE/'results'/'metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
