"""Run: python analysis/commission/analyze.py   (pandas required)"""
from pathlib import Path
import pandas as pd
file = Path(__file__).resolve().parents[2] / 'data' / 'synthetic_agent_commissions.csv'
df = pd.read_csv(file)
df['commission_ratio'] = df['total_commission_ngn'] / df['ggr_ngn'].where(df['ggr_ngn'] > 0)
df['review_flag'] = df['ggr_ngn'].le(0) | df['commission_ratio'].gt(.40)
summary = df.groupby(['month','product'], as_index=False).agg(
  stake_ngn=('stake_ngn','sum'),
  ggr_ngn=('ggr_ngn','sum'),
  commission_ngn=('total_commission_ngn','sum'),
  rows_for_review=('review_flag','sum'))
summary['commission_pct'] = 100*summary['commission_ngn']/summary['ggr_ngn'].where(summary['ggr_ngn']>0)
print(summary.round(2).to_string(index=False))
print('ROWS REQUIRING REVIEW:', int(df['review_flag'].sum()))
