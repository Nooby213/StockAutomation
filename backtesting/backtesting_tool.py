import pandas as pd
import matplotlib.pyplot as plt

d = pd.read_parquet('005930.parquet')

# 데이터
d['5d_max'] = d['close'].rolling(5).max()
d['5d_min'] = d['close'].rolling(5).min()
d['prev_close'] = d['close'].shift(1)
d['20d_ma'] = d['close'].rolling(20).mean()

# 파라미터 설정
holding_cash = 1000000  # 초기 자본금
position = 0  # 보유 주식 수
avg_price = 0  # 평균 매입 가격

daily_total_value = []  # 일별 총 자산 가치 기록

# for 문으로 하루씩 백테스팅 진행
for idx, data in d.iterrows():
    # 하루 시작
    daily_total_value.append(0)

    # 매수 조건 확인 및 매수
    if data['close'] < data['20d_ma'] and position == 0:
        holding_cash -= data['close']  # 주식 매수로 현금 감소
        avg_price = data['close']  # 매수 가격 기록
        position += 1  # 보유 주식 수 증가

    # 매도 조건 확인 및 매도
    elif position > 0:
        holding_cash += data['close']  # 주식 매도로 현금 증가
        avg_price = 0  # 평균 매입 가격 초기화
        position -= 1  # 보유 주식 수 감소

    # 장 마감 후
    daily_total_value[-1] = holding_cash + position * data['close']  # 총 자산 가치 계산

print('====== Daily Total Asset Value ====')
print(daily_total_value)

# 일별 총 자산 가치 그래프 출력
plt.figure(figsize=(15, 8))
plt.plot(daily_total_value, label='Total Asset Value')
plt.legend()
plt.show()