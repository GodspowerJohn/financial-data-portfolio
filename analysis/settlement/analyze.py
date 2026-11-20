"""Run: python analysis/settlement/analyze.py   (pandas required)"""
from pathlib import Path
import pandas as pd
file = Path(__file__).resolve().parents[2] / 'data' / 'synthetic_settlements.csv'
df = pd.read_csv(file)
expected = df['expected_settlement_ngn']
actual = df['bank_settlement_ngn'].fillna(0)
df['absolute_exposure_ngn'] = (expected - actual).abs()
df['is_matched'] = df['reconciliation_status'].eq('Matched')
summary = df.groupby(['month','provider'], as_index=False).agg(
    transaction_count=('transaction_id','count'),
    matched=('is_matched','sum'),
    exposure_ngn=('absolute_exposure_ngn','sum'),
)
summary['match_rate_pct'] = summary['matched'] / summary['transaction_count'] * 100
print(summary.round(2).to_string(index=False))
print('OVERALL MATCH RATE:', round(100*df['is_matched'].mean(),2), '%')
print('ABSOLUTE UNRECONCILED EXPOSURE:', round(df['absolute_exposure_ngn'].sum(),2), 'NGN')
