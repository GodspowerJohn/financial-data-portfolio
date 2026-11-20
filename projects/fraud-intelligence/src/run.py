"""Reproduce a transaction-monitoring experiment using invented synthetic transactions.
Run: python projects/fraud-intelligence/src/run.py
No real customer, employer, or bank data is included.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, average_precision_score

BASE = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(20261120)
n=4800
start = pd.Timestamp('2026-01-01')
minutes = np.sort(rng.integers(0, 240 * 24 * 60, n))
dates = start + pd.to_timedelta(minutes, unit='m')
amount = np.round(rng.lognormal(10.5, 1.05, n), 2)
amount = np.minimum(amount, 4_500_000)
prior_tx = rng.poisson(2.6, n)
new_device = rng.binomial(1, .13, n)
intl = rng.binomial(1, .10, n)
hour = dates.hour.to_numpy()
night = ((hour < 5) | (hour >= 23)).astype(int)
# Hidden fraud propensity is only for simulating labels, not used as a model feature.
log_odds = -5.0 + 2.5*new_device + 1.4*intl + 1.9*(amount>230000) + .7*night + 1.2*(prior_tx>5)
prob = 1/(1+np.exp(-log_odds))
fraud = rng.binomial(1, prob)
df = pd.DataFrame({
    'transaction_id':[f'TXN-{i+1:06d}' for i in range(n)],
    'event_time':dates.astype(str),
    'amount_ngn':amount,
    'prior_24h_transactions':prior_tx,
    'new_device':new_device,
    'cross_border':intl,
    'hour_of_day':hour,
    'is_fraud':fraud
})
(BASE/'data').mkdir(exist_ok=True)
(BASE/'results').mkdir(exist_ok=True)
df.to_csv(BASE/'data'/'transactions.csv',index=False)
# Chronological split prevents future records appearing in the training set.
i1=int(.60*n);i2=int(.80*n)
feature_cols=['amount_ngn','prior_24h_transactions','new_device','cross_border','hour_of_day']
X=df[feature_cols]
y=df['is_fraud']
model=Pipeline([('scale',StandardScaler()),('model',LogisticRegression(class_weight='balanced',max_iter=300,random_state=42))])
model.fit(X.iloc[:i1],y.iloc[:i1])
val_prob=model.predict_proba(X.iloc[i1:i2])[:,1]
# Threshold chosen ONLY on validation, not the test set. Maximize F1 for illustration.
thresholds=np.linspace(.15,.90,31)
chosen=max(thresholds,key=lambda t:f1_score(y.iloc[i1:i2],val_prob>=t,zero_division=0))
test_prob=model.predict_proba(X.iloc[i2:])[:,1]
ytest=y.iloc[i2:]
pred=(test_prob>=chosen).astype(int)
tn,fp,fn,tp=confusion_matrix(ytest,pred,labels=[0,1]).ravel()
# Simple baseline rule on same test period, not trained.
rule=((X.iloc[i2:]['new_device']==1)&(X.iloc[i2:]['amount_ngn']>230000)).astype(int)
metrics={
    'sample_transactions':n,'fraud_cases':int(y.sum()),'fraud_rate':round(float(y.mean()),4),
    'train_rows':i1,'validation_rows':i2-i1,'test_rows':n-i2,'threshold':round(float(chosen),3),
    'precision':round(float(precision_score(ytest,pred,zero_division=0)),4),
    'recall':round(float(recall_score(ytest,pred,zero_division=0)),4),
    'f1':round(float(f1_score(ytest,pred,zero_division=0)),4),
    'average_precision':round(float(average_precision_score(ytest,test_prob)),4),
    'tp':int(tp),'fp':int(fp),'tn':int(tn),'fn':int(fn),
    'test_fraud_cases':int(ytest.sum()),'test_flagged':int(pred.sum()),
    'rule_precision':round(float(precision_score(ytest,rule,zero_division=0)),4),
    'rule_recall':round(float(recall_score(ytest,rule,zero_division=0)),4),
    'false_positive_rate':round(float(fp/max(1,fp+tn)),4),
    'review_amount_ngn':round(float(df.iloc[i2:].loc[pred==1,'amount_ngn'].sum()),2),
    'missed_fraud_amount_ngn':round(float(df.iloc[i2:].loc[(ytest.to_numpy()==1)&(pred==0),'amount_ngn'].sum()),2),
}
(BASE/'results'/'metrics.json').write_text(json.dumps(metrics,indent=2))
# Publish no predictions containing identifying data; transactions are synthetic IDs only.
print(json.dumps(metrics,indent=2))
