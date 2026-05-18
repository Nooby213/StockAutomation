import pandas as pd

# 1. pandas 기본
# py -m pip install pandas

# 2. DataFrame 만들기
# 방법 1: 빈 DataFrame을 만들고 column 추가
df = pd.DataFrame()

df["Name"] = ["Jacky", "Steven", "George"]
df["Age"] = [38, 25, 23]
df["Driver"] = [True, False, True]

print("=== DataFrame 생성 방법 1 ===")
print(df)
print()


# 방법 2: dictionary로 DataFrame 만들기
data = {
    "Name": ["Jacky", "Steven", "George"],
    "Age": [38, 25, 23],
    "Driver": [True, False, True]
}

df = pd.DataFrame(data)

print("=== DataFrame 생성 방법 2 ===")
print(df)
print()


# 3. DataFrame 구성요소

# DataFrame: 행과 열로 이루어진 2차원 데이터
# Series: DataFrame의 각 column
# Index: 행을 구분하는 이름 또는 번호

print("=== Age column 출력 ===")
print(df["Age"])
print()

print("=== 자료형 확인 ===")
print(type(df))
print(type(df["Age"]))
print()

print("=== index 확인 ===")
print(df.index)
print()


# index 이름 설정
df.index.name = "index"

print("=== index 이름 설정 ===")
print(df)
print()


# index 재설정
# 기존 index가 새로운 column으로 들어가고, 새로운 숫자 index가 생긴다.
reset_df = df.reset_index()

print("=== index 재설정 ===")
print(reset_df)
print()

# 4. Column 추가, 수정, 삭제

data = {
    "Name": ["Jacky", "Steven", "George"],
    "Age": [38, 25, 23],
    "Driver": [True, False, True]
}

df = pd.DataFrame(data)
df.index = ["a", "b", "c"]
df.index.name = "index"

print("=== 원본 DataFrame ===")
print(df)
print()


# column 추가
df["Location"] = ["Area 1", "Area 2", "Area 3"]

print("=== Location column 추가 ===")
print(df)
print()


# column 이름 변경
df = df.rename(columns={"Name": "Person"})

print("=== Name column을 Person으로 변경 ===")
print(df)
print()


# column 삭제
df = df.drop(columns="Location")

print("=== Location column 삭제 ===")
print(df)
print()

# 5. Row 데이터 추가

data = {
    "Name": ["Jacky", "Steven", "George"],
    "Age": [38, 25, 23],
    "Driver": [True, False, True]
}

df = pd.DataFrame(data)
df.index = ["a", "b", "c"]
df.index.name = "index"

print("=== 원본 DataFrame ===")
print(df)
print()


# 추가할 row를 DataFrame으로 생성
new_data = {
    "Name": ["Harry"],
    "Age": [10],
    "Driver": [True]
}

new_df = pd.DataFrame(new_data, index=["d"])

print("=== 추가할 row ===")
print(new_df)
print()


# 기존 DataFrame과 새 DataFrame 합치기
df = pd.concat([df, new_df])

print("=== row 추가 결과 ===")
print(df)
print()

# 6. DataFrame 인덱싱

data = {
    "Name": ["Jacky", "Steven", "George"],
    "Age": [38, 25, 23],
    "Driver": [True, False, True]
}

df = pd.DataFrame(data)
df.index = ["a", "b", "c"]
df.index.name = "index"

print("=== 인덱싱용 DataFrame ===")
print(df)
print()


# 6-1. [] 인덱싱

# 특정 column 선택
print("=== Name column 선택 ===")
print(df["Name"])
print()

# 여러 column 선택
print("=== Name, Driver column 선택 ===")
print(df[["Name", "Driver"]])
print()

# 여러 row 선택
print("=== 0번째부터 1번째 row까지 선택 ===")
print(df[0:2])
print()

# 6-2. loc 인덱싱

# loc는 index 이름과 column 이름으로 접근한다.
print("=== loc로 index가 a인 row 선택 ===")
print(df.loc["a"])
print()

print("=== loc로 a행의 Name 값 선택 ===")
print(df.loc["a", "Name"])
print()

# 6-3. iloc 인덱싱

# iloc는 숫자 위치로 접근한다.
print("=== iloc로 2번째 row 선택 ===")
print(df.iloc[1])
print()

print("=== iloc로 2번째 row의 Age 값 선택 ===")
print(df.iloc[1]["Age"])
print(df.iloc[1, 1])
print()


# 6-4. Boolean 인덱싱

# 조건에 맞는 row만 필터링할 때 사용한다.
print("=== Age가 25 이상인지 확인 ===")
print(df["Age"] >= 25)
print()

print("=== Age가 25 이상인 row만 선택 ===")
print(df[df["Age"] >= 25])
print()


# 6-5. at, iat 인덱싱

# at: index 이름과 column 이름으로 하나의 값에 접근
print("=== at으로 a행 Driver 값 선택 ===")
print(df.at["a", "Driver"])
print()

# iat: 숫자 위치로 하나의 값에 접근
print("=== iat으로 0행 2열 값 선택 ===")
print(df.iat[0, 2])
print()

# 특정 cell 값 수정
df.at["a", "Driver"] = False

print("=== a행 Driver 값 수정 ===")
print(df)
print()


# 7. CSV 파일 읽고 쓰기

# CSV 파일 읽기
# index_col=0은 첫 번째 column을 index로 사용한다는 뜻이다.

csv_data = pd.read_csv("./dataset/yfinance_aapl.csv", index_col=0)
print(csv_data.head(3))


# CSV 파일로 저장

csv_data.to_csv("./dataset/test.csv")


# 8. Excel 파일 읽고 쓰기

# Excel 파일을 사용하려면 openpyxl 설치 필요:
# py -m pip install openpyxl

# Excel 파일 읽기

excel_data = pd.read_excel(
    "./dataset/yfinance_aapl.xlsx",
    sheet_name="aapl",
    engine="openpyxl",
    index_col=0
)

print(excel_data.head(3))


# Excel 파일로 저장

excel_data.to_excel(
    "./dataset/yfinance_aapl_result.xlsx",
    sheet_name="aapl",
    engine="openpyxl"
)