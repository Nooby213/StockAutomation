import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

ticker = "SPY"
start_date = "2024-01-01"
monthly_budget = 1_000_000
usdkrw = 1400
df = yf.download(ticker, start=start_date, auto_adjust=True)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
df.dropna(inplace=True)

df["MA20"] = df["Close"].rolling(window=20).mean()
df["month"] = df.index.to_period("M")

# 원화를 달러로 환산
monthly_budget_usd = monthly_budget / usdkrw


# 전략 1: 월 1회 매수
# 조건: Close < MA20 인 날 중 그 달 최저 Close 매수
monthly_buy_records = []

for month, month_df in df.groupby("month"):
    candidates = month_df[month_df["Close"] < month_df["MA20"]]

    # 해당 월에 조건 만족하는 날이 없으면 매수 안 함
    if candidates.empty:
        continue

    # 조건 만족일 중 Close가 가장 낮은 날
    buy_date = candidates["Close"].idxmin()
    buy_price = candidates.loc[buy_date, "Close"]

    shares = monthly_budget_usd / buy_price

    monthly_buy_records.append({
        "date": buy_date,
        "price": buy_price,
        "invest_usd": monthly_budget_usd,
        "shares": shares
    })

monthly_buys = pd.DataFrame(monthly_buy_records)


# 전략 2: 매주 월요일 매수
# 매달 100만원을 그 달 월요일 개수로 나눠 매수
weekly_buy_records = []

for month, month_df in df.groupby("month"):
    monday_df = month_df[month_df.index.weekday == 0]

    if monday_df.empty:
        continue

    weekly_budget_usd = monthly_budget_usd / len(monday_df)

    for buy_date, row in monday_df.iterrows():
        buy_price = row["Close"]
        shares = weekly_budget_usd / buy_price

        weekly_buy_records.append({
            "date": buy_date,
            "price": buy_price,
            "invest_usd": weekly_budget_usd,
            "shares": shares
        })

weekly_buys = pd.DataFrame(weekly_buy_records)


# 누적 수익률 계산 함수
def make_portfolio(df, buys):
    result = df.copy()
    result["invest_usd"] = 0.0
    result["buy_shares"] = 0.0

    for _, row in buys.iterrows():
        result.loc[row["date"], "invest_usd"] += row["invest_usd"]
        result.loc[row["date"], "buy_shares"] += row["shares"]

    result["total_invest_usd"] = result["invest_usd"].cumsum()
    result["total_shares"] = result["buy_shares"].cumsum()
    result["portfolio_value_usd"] = result["total_shares"] * result["Close"]

    result["profit_usd"] = result["portfolio_value_usd"] - result["total_invest_usd"]
    result["return_pct"] = result["profit_usd"] / result["total_invest_usd"] * 100

    return result


monthly_result = make_portfolio(df, monthly_buys)
weekly_result = make_portfolio(df, weekly_buys)


# 최종 결과 출력
last_date = df.index[-1]

monthly_final = monthly_result.loc[last_date]
weekly_final = weekly_result.loc[last_date]

print("====== 월 1회 조건 매수 전략 ======")
print(f"총 투자금: ${monthly_final['total_invest_usd']:,.2f}")
print(f"평가금액: ${monthly_final['portfolio_value_usd']:,.2f}")
print(f"수익금: ${monthly_final['profit_usd']:,.2f}")
print(f"수익률: {monthly_final['return_pct']:.2f}%")
print(f"매수 횟수: {len(monthly_buys)}회")

print("\n====== 매주 월요일 매수 전략 ======")
print(f"총 투자금: ${weekly_final['total_invest_usd']:,.2f}")
print(f"평가금액: ${weekly_final['portfolio_value_usd']:,.2f}")
print(f"수익금: ${weekly_final['profit_usd']:,.2f}")
print(f"수익률: {weekly_final['return_pct']:.2f}%")
print(f"매수 횟수: {len(weekly_buys)}회")


# 그래프 1: 평가금액 비교
plt.figure(figsize=(15, 7))
plt.plot(monthly_result.index, monthly_result["portfolio_value_usd"], label="Monthly condition buy")
plt.plot(weekly_result.index, weekly_result["portfolio_value_usd"], label="Weekly Monday buy")
plt.title("Portfolio Value Comparison")
plt.xlabel("Date")
plt.ylabel("Portfolio Value USD")
plt.legend()
plt.grid(True)
plt.show()


# 그래프 2: 수익률 비교
plt.figure(figsize=(15, 7))
plt.plot(monthly_result.index, monthly_result["return_pct"], label="Monthly condition buy")
plt.plot(weekly_result.index, weekly_result["return_pct"], label="Weekly Monday buy")
plt.title("Return Percentage Comparison")
plt.xlabel("Date")
plt.ylabel("Return %")
plt.legend()
plt.grid(True)
plt.show()


# 그래프 3: 매수 지점 표시
plt.figure(figsize=(15, 7))
plt.plot(df.index, df["Close"], label="Close")
plt.plot(df.index, df["MA20"], label="MA20")

plt.scatter(monthly_buys["date"], monthly_buys["price"], label="Monthly Buy", marker="o")
plt.scatter(weekly_buys["date"], weekly_buys["price"], label="Weekly Monday Buy", marker="x")

plt.title(f"{ticker} Buy Points")
plt.xlabel("Date")
plt.ylabel("Price USD")
plt.legend()
plt.grid(True)
plt.show()