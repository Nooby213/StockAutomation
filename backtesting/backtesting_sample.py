import pandas as pd
import matplotlib.pyplot as plt

d = pd.read_parquet('005930.parquet')
print('====== Original Data ====')
print(d)
print()

d['5d_max'] = d.rolling(5)['close'].max()
print('====== Data with 5-Day Max ====')
print(d)
print()

d['5d_min'] = d.rolling(5)['close'].min()
print('====== Data with 5-Day Min ====')
print(d)
print()

d['last_close'] = d['close'].shift(1)
print('====== Data with Last Close ====')
print(d)
print()

d['20d_mean'] = d.rolling(20)['close'].mean()
print('====== Data with 20-Day Mean ====')
print(d)
print()