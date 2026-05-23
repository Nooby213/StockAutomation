import pandas as pd
import matplotlib.pyplot as plt

# 종가가 3일 최저가 & 20일 이평선 아래
# 지금 진입해 있는 포지션이 없을 때
d = pd.read_parquet('005930.parquet')

# 파라미터 설정
holding_cash = 1000000  # 초기 자본금
position = 0  # 보유 주식 수
avg_price = 0  # 평균 매입 가격
daily_total_value = []  # 일별 총 자산 가치 기록
holding_time_passed = 0  # 보유 기간 기록

# for 문으로 하루씩 백테스팅 진행
for idx, data in d.iterrows():
    # 하루 시작
    daily_total_value.append(0)
    
    # 전략 구현
    # 종가가 3일 최저가이고 20일 이평 아래인지 여부
    # 현재 매수 가능한 현금이 있는지
    # 매수 조건에 맞으면 매수
    if (data['close'] == d['close'].rolling(window=3).min().iloc[idx]) and (data['close'] < d['close'].rolling(window=20).mean().iloc[idx]) and (holding_cash >= data['close']):
        if holding_cash >= data['close'] and position == 0:  # 매수 조건에 맞고, 현재 포지션이 없을 때
            position += 1  # 주식 1주 매수
            holding_cash -= data['close']  # 매수 금액 차감
            avg_price = data['close']  # 평균 매입 가격 계산
            holding_time_passed = 0  # 보유 기간 초기화

    # 마지막 매수 3일 후 매도
    if position > 0 and holding_time_passed >= 3:  # 포지션이 있을 때
        holding_cash += position * data['close']  # 매도 금액 추가
        position = 0  # 포지션 초기화
        avg_price = 0  # 평균 매입 가격 초기화
    # 하루 마무리
    daily_total_value[-1] = holding_cash + position * data['close']  # 총 자산 가치 계산
    # 파라미터 업데이트
    if position > 0:
        holding_time_passed += 1  # 보유 기간 증가

# 결과 시각화
plt.figure(figsize=(15, 8))
plt.plot(d.index, daily_total_value, label='Total Asset Value')
plt.title('Backtesting Strategy Performance')
plt.xlabel('Date')
plt.ylabel('Total Asset Value')
plt.legend()
plt.grid()
plt.show()

return1 = daily_total_value.copy()