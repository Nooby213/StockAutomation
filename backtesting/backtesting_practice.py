import pandas as pd
import matplotlib.pyplot as plt 

d = pd.read_parquet("005930.parquet")

# 오늘 포함 과거 5일 종가 중 최고값
d['5d_max'] = d['close'].rolling(5).max()

# 오늘 포함 과거 5일 종가 중 최저값
d['5d_min'] = d['close'].rolling(5).min()

# 전일 종가
d['prev_close'] = d['close'].shift(1)

# 20일 이동평균
d['20d_ma'] = d['close'].rolling(20).mean()

print(d.head(10))
print()

# 매수 시점
buy = d[(d['close'] == d['5d_min']) & (d['close'] < d['20d_ma'])]
print('====== Buy Signal ====')
print(buy)
print()

# plt.plot을 활용해 주가 그래프 출력
# plt.figure(figsize=(15, 8))
plt.plot(d['close'], label='Close Price')
plt.legend()
# plt.show()

# 주가 그래프에 매수 시점 표시
plt.plot(d['close'], label='Close Price')
plt.scatter(buy.index, buy['close'], color='red', label='Buy Signal', marker='^')
plt.legend()
# plt.show()

# 최근 300일만 매수 타점 표시
d_sample = d[-300:]
buy_sample = d_sample[(d_sample['close'] == d_sample['5d_min']) & (d_sample['close'] < d_sample['20d_ma'])]
print('====== Recent 300 Days Buy Signal ====')
print(buy_sample)
print()

plt.figure(figsize=(15, 8))
plt.plot(d_sample['close'], label='Close Price')
plt.scatter(buy_sample.index, buy_sample['close'], color='red', label='Buy Signal', marker='^')
plt.legend()
plt.show()
