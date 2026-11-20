"""Synthetic 36-month P&L and six-month liquidity scenarios, with holdout backtest.
Run: python projects/cashflow-forecast/src/run.py
"""
from pathlib import Path
import numpy as np,pandas as pd,json
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
BASE=Path(__file__).resolve().parents[1];rng=np.random.default_rng(2602)
periods=pd.period_range('2023-10','2026-09',freq='M');n=len(periods)
t=np.arange(n);season=np.sin(2*np.pi*(t%12)/12)
rev=np.maximum(0,26_000_000+430_000*t+2_300_000*season+rng.normal(0,1_100_000,n))
variable=rev*(.42+rng.normal(0,.016,n));fixed=8_300_000+75_000*t+rng.normal(0,225_000,n)
capex=np.maximum(0,1_100_000+rng.normal(0,300_000,n));wc=np.maximum(-2_000_000,rng.normal(300_000,600_000,n))
ebitda=rev-variable-fixed
netcash=ebitda-capex-wc
cash=14_000_000+np.cumsum(netcash)
df=pd.DataFrame({'month':[str(x) for x in periods],'revenue_ngn':rev.round(2),'variable_cost_ngn':variable.round(2),'fixed_cost_ngn':fixed.round(2),'ebitda_ngn':ebitda.round(2),'capex_ngn':capex.round(2),'working_capital_increase_ngn':wc.round(2),'net_cashflow_ngn':netcash.round(2),'ending_cash_ngn':cash.round(2)})
(BASE/'data').mkdir(exist_ok=True);(BASE/'results').mkdir(exist_ok=True)
df.to_csv(BASE/'data'/'monthly_financials.csv',index=False)
# A simple time + sine/cosine seasonal regression; last 6 months are an untouched holdout.
def features(idx):
 a=np.asarray(idx,dtype=float)
 return np.column_stack([a,np.sin(2*np.pi*a/12),np.cos(2*np.pi*a/12)])
split=n-6
model=Ridge(alpha=2.0).fit(features(t[:split]),rev[:split]);holdout=model.predict(features(t[split:]))
mae=float(mean_absolute_error(rev[split:],holdout));future_idx=np.arange(n,n+6)
# Refit on all observed months only after recording holdout performance.
forecast_model=Ridge(alpha=2.0).fit(features(t),rev)
base=np.maximum(0,forecast_model.predict(features(future_idx)))
vc_ratio=float(variable[-12:].sum()/rev[-12:].sum());fixed_mean=float(fixed[-6:].mean());capex_mean=float(capex[-12:].mean());wc_mean=float(wc[-12:].mean())
rows=[]
for scenario,mult in [('Downside',.88),('Base',1.00),('Upside',1.12)]:
 c=float(cash[-1]);
 for j,(period,amount) in enumerate(zip(pd.period_range(periods[-1]+1,periods[-1]+6,freq='M'),base)):
  forecast_rev=round(float(amount*mult),2);forecast_ebitda=forecast_rev*(1-vc_ratio)-fixed_mean
  net=forecast_ebitda-capex_mean-wc_mean;c+=net
  rows.append([str(period),scenario,forecast_rev,round(float(forecast_ebitda),2),round(float(net),2),round(float(c),2)])
future=pd.DataFrame(rows,columns=['month','scenario','forecast_revenue_ngn','forecast_ebitda_ngn','forecast_net_cashflow_ngn','forecast_ending_cash_ngn'])
future.to_csv(BASE/'data'/'forecast_scenarios.csv',index=False)
metrics={'history_months':n,'backtest_months':6,'revenue_mae_ngn':round(mae,2),'latest_month_revenue_ngn':round(float(rev[-1]),2),
'latest_month_ebitda_ngn':round(float(ebitda[-1]),2),'latest_cash_ngn':round(float(cash[-1]),2),
'historical_ebitda_margin':round(float(ebitda.sum()/rev.sum()),4),
'next_six_months_revenue_by_scenario_ngn':future.groupby('scenario').forecast_revenue_ngn.sum().round(2).to_dict(),
'forecast_cash_at_six_months_ngn':future.groupby('scenario').tail(1).set_index('scenario').forecast_ending_cash_ngn.to_dict(),
'assumptions':{'downside_revenue_multiplier':.88,'upside_revenue_multiplier':1.12,'variable_cost_ratio':round(vc_ratio,4)}}
(BASE/'results'/'metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
