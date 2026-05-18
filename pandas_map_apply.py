import pandas as pd

# 1. map, apply를 사용하여 DataFrame에 함수 적용하기
# map은 각 요소를 변환할 때 사용한다.
# apply는 Series 또는 DataFrame의 행/열 단위로 함수를 적용할 때 사용한다.


# 2. Python에서 map 사용하기

# 리스트의 각 숫자 제곱하기
numbers = [1, 2, 3, 4, 5]

print("=== 리스트 컴프리헨션으로 각 숫자 제곱 ===")
print([num ** 2 for num in numbers])
print()


# map을 사용해서 리스트의 각 숫자 제곱하기
def square(number):
    return number ** 2


squared_numbers = map(square, numbers)

print("=== map으로 각 숫자 제곱 ===")
print(list(squared_numbers))
print()


# 3. pandas에서 map 함수 사용하기
# pandas의 map은 Series에만 적용 가능하다.

# 예제 Series 생성
s = pd.Series([1, 2, 3])

print("=== 원본 Series ===")
print(s)
print()


# 각 원소에 10을 곱하는 함수
def multiply_by_ten(x):
    return x * 10


# Series의 각 원소에 함수 적용
result_series = s.map(multiply_by_ten)

print("=== Series.map으로 각 원소에 10 곱하기 ===")
print(result_series)
print()


# 사전을 사용한 매핑
s = pd.Series(["apple", "banana", "carrot"])
fruit_colors = {
    "apple": "red",
    "banana": "yellow",
    "carrot": "orange"
}

result_fruit_colors = s.map(fruit_colors)

print("=== dictionary를 사용한 Series.map 매핑 ===")
print(result_fruit_colors)
print()


# 4. pandas에서 apply 함수 사용하기
# apply는 DataFrame의 행 또는 열에 함수를 적용할 수 있다.

df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [10, 13, 15]
})

print("=== apply 예제 DataFrame ===")
print(df)
print()


# 최대값, 최소값의 차이를 구하는 함수 정의
def diff_max_min(x):
    return x.max() - x.min()


# axis=0: 함수가 각 column에 독립적으로 적용된다.
print("=== apply axis=0, column별 max - min ===")
print(df.apply(diff_max_min, axis=0))
print()

# axis=1: 함수가 각 row에 독립적으로 적용된다.
print("=== apply axis=1, row별 max - min ===")
print(df.apply(diff_max_min, axis=1))
print()


# 5. apply를 사용하여 새로운 column 생성하기

df = pd.DataFrame({
    "name": ["John", "Lucy", "Mark", "Jane"],
    "age": [28, 22, 35, 15]
})

print("=== 나이 카테고리 예제 DataFrame ===")
print(df)
print()


# 나이에 따라 카테고리를 지정하는 함수
def age_category(age):
    if age < 18:
        return "Underage"
    elif age < 30:
        return "Young"
    else:
        return "Adult"


# age column에 함수를 적용하여 age_category column 생성
df["age_category"] = df["age"].apply(age_category)

print("=== apply로 age_category column 추가 ===")
print(df)
print()
