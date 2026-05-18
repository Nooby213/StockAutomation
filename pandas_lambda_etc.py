import pandas as pd
from pathlib import Path

# 1. lambda 사용하기
# lambda는 이름 없는 간단한 함수를 만들 때 사용한다.
# 기본 문법: lambda arguments: expression

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"


# 2. Python lambda 기본 예제

# 간단한 덧셈 함수
add = lambda x, y: x + y

print("=== lambda 덧셈 함수 ===")
print(add(5, 3))
print()


# 리스트 정렬 시 key 함수로 사용
points = [(1, 2), (3, 1), (5, 4)]
points.sort(key=lambda point: point[1])

print("=== lambda를 사용하여 tuple의 2번째 값 기준 정렬 ===")
print(points)
print()


# map 함수와 함께 사용하여 각 요소에 연산 적용
nums = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, nums)

print("=== map + lambda로 각 숫자 제곱 ===")
print(list(squared))
print()


# filter 함수와 함께 사용하여 조건을 만족하는 요소 필터링
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
evens = filter(lambda x: x % 2 == 0, nums)

print("=== filter + lambda로 짝수만 필터링 ===")
print(list(evens))
print()


# 3. Pandas에서 lambda 사용하기
# lambda는 apply, map 등과 함께 자주 사용된다.

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

print("=== 원본 DataFrame ===")
print(df)
print()


# apply로 특정 column에 적용하기
# A column의 각 값에 10을 더한다.
df["A"] = df["A"].apply(lambda x: x + 10)

print("=== A column에 10 더하기 ===")
print(df)
print()


# 조건에 따른 새로운 column 생성하기
df["C"] = df["A"].apply(lambda x: "large" if x > 11 else "small")

print("=== 조건에 따라 C column 생성 ===")
print(df)
print()


# DataFrame의 여러 column에 함수 적용하기
# axis=1은 row 단위로 함수를 적용한다.
df["sum"] = df.apply(lambda row: row["A"] + row["B"], axis=1)

print("=== row 단위로 A + B 계산하여 sum column 생성 ===")
print(df)
print()


# Series에서 특정 조건을 만족하는 요소 필터링하기
s = pd.Series([1, 2, 3, 4, 5])
filtered_s = s[s.apply(lambda x: x > 2)]

print("=== Series에서 2보다 큰 값만 필터링 ===")
print(filtered_s)
print()


# 4. lambda 또는 Python 함수를 사용해서 가격변동률 계산하기
# 가격변동률 = ((Close - Open) / Open) * 100

data = pd.read_csv(DATASET_DIR / "yfinance_aapl.csv", index_col=0)

print("=== AAPL CSV 데이터 상위 3개 ===")
print(data.head(3))
print()

# lambda를 사용하여 가격변동률 column 생성
data["PriceChangePercent"] = data.apply(
    lambda row: ((row["Close"] - row["Open"]) / row["Open"]) * 100,
    axis=1
)

print("=== lambda로 계산한 PriceChangePercent 상위 5개 ===")
print(data["PriceChangePercent"].head())
print()


# 일반 함수를 사용하여 가격변동률 column 생성
def calculate_price_change_percent(row):
    return ((row["Close"] - row["Open"]) / row["Open"]) * 100


data = pd.read_csv(DATASET_DIR / "yfinance_aapl.csv", index_col=0)
data["PriceChangePercent"] = data.apply(calculate_price_change_percent, axis=1)

print("=== 일반 함수로 계산한 PriceChangePercent 상위 5개 ===")
print(data["PriceChangePercent"].head())
print()


# 5. 기타 중요한 pandas 기능들

# 5-1. reset_index()
# reset_index()는 DataFrame의 index를 기본 정수 index로 재설정할 때 사용한다.

df = pd.read_csv(DATASET_DIR / "yfinance_aapl.csv", index_col=0)

print("=== reset_index 예제 데이터 상위 3개 ===")
print(df.head(3))
print()

# Date column을 index로 설정한다.
# 이미 Date가 index라면 이 부분은 필요 없을 수 있다.
if "Date" in df.columns:
    df = df.set_index("Date")

print("=== Date를 index로 설정한 결과 상위 3개 ===")
print(df.head(3))
print()

# reset_index()로 정수 index로 치환
# 이때 기존 index는 새로운 column으로 추가된다.
df = df.reset_index()

print("=== reset_index 결과 ===")
print(df.head())
print()

# 특정 row를 지운 다음 reset_index로 index 재조정하기
print("=== index 1, 2 제거 후 reset_index ===")
print(df.drop(index=[1, 2]).reset_index())
print()

# reset_index(drop=True)로 기존 index가 새로운 column으로 추가되지 않게 하기
print("=== index 1, 2 제거 후 reset_index(drop=True) ===")
print(df.drop(index=[1, 2]).reset_index(drop=True))
print()


# 5-2. pd.concat()
# pd.concat()은 하나 이상의 DataFrame을 행 또는 열 기준으로 합칠 때 사용한다.

df_aapl = pd.read_csv(DATASET_DIR / "yfinance_aapl_3year.csv", index_col=0).head(5)
df_nvda = pd.read_csv(DATASET_DIR / "yfinance_nvda_3year.csv", index_col=0).head(5)

print("=== AAPL 3년 데이터 상위 5개 ===")
print(df_aapl)
print()

print("=== NVDA 3년 데이터 상위 5개 ===")
print(df_nvda)
print()

# DataFrame을 가로로 연결하기
print("=== pd.concat axis=1, 가로로 연결 ===")
print(pd.concat([df_aapl, df_nvda], axis=1))
print()

# DataFrame을 세로로 연결하기
print("=== pd.concat axis=0, 세로로 연결 ===")
print(pd.concat([df_aapl, df_nvda], axis=0))
print()

# 새로운 index를 자동으로 붙이기
print("=== pd.concat axis=0, ignore_index=True ===")
print(pd.concat([df_aapl, df_nvda], axis=0, ignore_index=True))
print()
