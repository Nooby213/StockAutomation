import pandas as pd
import numpy as np
from pathlib import Path

# 1. pandas를 사용한 데이터 연산
# Series를 사용하면 column 단위로 산술연산, 통계연산, 정렬 등을 할 수 있다.

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

# CSV 파일 읽기
# index_col=0은 첫 번째 column을 index로 사용한다는 뜻이다.
data = pd.read_csv(DATASET_DIR / "yfinance_aapl.csv", index_col=0)

print("=== CSV 데이터 상위 3개 ===")
print(data.head(3))
print()

print("=== 데이터 정보 요약 ===")
print(data.describe())
print()


# 2. 산술연산
# Series 객체는 +, -, *, / 등의 연산자를 사용하여 산술 연산을 수행할 수 있다.
# 같은 index끼리 계산된다.

print("=== Open / Close 산술연산 ===")
print(data["Open"] / data["Close"])
print()


# 3. 통계연산
# mean, sum, min, max 등의 통계 메서드를 사용할 수 있다.

print("=== Open 평균 ===")
print(data["Open"].mean())
print()

print("=== Open 전체 합계 ===")
print(data["Open"].sum())
print()

print("=== Open 최댓값 ===")
print(data["Open"].max())
print()

print("=== Open 최솟값 ===")
print(data["Open"].min())
print()


# 매일 시초에 사서 고가에 팔았을 때를 가정하여 수익률 계산하기
profit = data["High"] / data["Open"]

print("=== 일별 수익률 High / Open 상위 5개 ===")
print(profit.head(5))
print()

# cumprod()를 사용하여 누적 수익률 계산하기
print("=== 누적 수익률 상위 5개 ===")
print(profit.cumprod().head(5))
print()

print("=== 원본 데이터 상위 3개 ===")
print(data.head(3))
print()

# diff()를 사용하여 이전 데이터와의 차이 계산하기
print("=== Open 전날과의 차이 ===")
print(data["Open"].diff().head(5))
print()

print("=== Open 이틀 전과의 차이 ===")
print(data["Open"].diff(2).head(5))
print()


# 4. 정렬
# sort_values: 값 기준 정렬
# sort_index: index 기준 정렬

print("=== Volume 기준 오름차순 정렬 ===")
print(data.sort_values(by="Volume").head())
print()

print("=== Volume 기준 내림차순 정렬 ===")
print(data.sort_values(by="Volume", ascending=False).head())
print()

print("=== Volume 내림차순 정렬 후 index 기준 재정렬 ===")
print(data.sort_values(by="Volume", ascending=False).sort_index().head())
print()

print("=== Open column 값 기준 오름차순 정렬 ===")
print(data["Open"].sort_values().head())
print()


# 5. 결측치 NaN 데이터 처리하기
# 결측치는 데이터가 누락되었거나 사용할 수 없음을 의미한다.

df = pd.DataFrame({
    "A": [1, 2, np.nan, 4],
    "B": [5, np.nan, np.nan, 8],
    "C": [10, 20, 30, 40]
})

print("=== 결측치가 있는 DataFrame ===")
print(df)
print()


# 5-1. 결측치 확인하기

print("=== 전체 데이터셋에 결측치가 하나라도 있는지 확인 ===")
print(df.isnull().values.any())
print()

print("=== 각 column별 결측치 개수 ===")
print(df.isnull().sum())
print()


# 5-2. 결측치 데이터 채우기

# 모든 결측치를 0으로 채우기
df_filled_zero = df.fillna(0)

print("=== 모든 결측치를 0으로 채우기 ===")
print(df_filled_zero)
print()

# 특정 값으로 결측치 대체하기
df_replaced = df.replace(np.nan, -1)

print("=== 모든 결측치를 -1로 대체하기 ===")
print(df_replaced)
print()

# 결측치를 앞 방향 값으로 채우기
df_filled_forward = df.ffill()

print("=== 결측치를 앞 방향 값으로 채우기 ===")
print(df_filled_forward)
print()

# 결측치를 뒷 방향 값으로 채우기
df_filled_backward = df.bfill()

print("=== 결측치를 뒷 방향 값으로 채우기 ===")
print(df_filled_backward)
print()

# 특정 column의 결측치를 해당 column의 평균값으로 채우기
df_filled_mean = df.copy()
df_filled_mean["B"] = df_filled_mean["B"].fillna(df_filled_mean["B"].mean())

print("=== B column 결측치를 B 평균값으로 채우기 ===")
print(df_filled_mean)
print()


# 5-3. 결측치를 보유한 행이나 열 제거하기

df = pd.DataFrame({
    "A": [1, 2, np.nan, 4],
    "B": [5, np.nan, np.nan, 8],
    "C": [10, 20, 30, 40]
})

print("=== 결측치 제거용 원본 DataFrame ===")
print(df)
print()

print("=== 결측치가 하나라도 있는 row 제거 ===")
print(df.dropna())
print()

print("=== 결측치가 하나라도 있는 column 제거 ===")
print(df.dropna(axis=1))
print()

print("=== index 1, 2번 row 제거 ===")
print(df.drop(index=[1, 2]))
print()
