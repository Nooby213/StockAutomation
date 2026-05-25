# backtest_laor_vs_monday.py

import math
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# 설정값

TICKER = "TQQQ"          # "TQQQ", "QLD", "QQQ" 등으로 변경
START_DATE = "2011-01-01"
END_DATE = None          # None이면 오늘까지

INITIAL_CASH = 15000     # 최초 투자금. 달러 기준
WEEKLY_CONTRIBUTION = 0  # 매주 추가입금. 적립식이면 예: 100
MONDAY_BUY_AMOUNT = 300  # 월요일 매수법: 매주 월요일마다 사는 금액

ALLOW_FRACTIONAL = True  # 소수점 주식 허용
TAX_RATE = 0.0           # 실현이익 세금. 대략 반영하려면 0.22 등 입력

# 라오어식 파라미터
LAOR_DIVISIONS = 40      # 현금을 몇 등분해서 살지
LAOR_TAKE_PROFIT = 0.10  # 평균단가 대비 +10% 도달 시 전량매도
LAOR_MAX_BUYS = 40       # 한 사이클 최대 매수 횟수. None이면 계속 매수 가능


# 데이터 다운로드

def load_price_data(ticker: str, start: str, end=None) -> pd.DataFrame:
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError("가격 데이터를 가져오지 못했습니다.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df[["Close"]].copy()
    df = df.dropna()
    df.index = pd.to_datetime(df.index)
    return df


# 공통 함수

def buy_shares(cash: float, shares: float, cost_basis: float, price: float, amount: float):
    """
    amount만큼 매수.
    반환: cash, shares, cost_basis, 실제매수금액
    """
    spend = min(cash, amount)

    if spend <= 0:
        return cash, shares, cost_basis, 0.0

    if ALLOW_FRACTIONAL:
        qty = spend / price
        actual_spend = spend
    else:
        qty = math.floor(spend / price)
        actual_spend = qty * price

    if qty <= 0:
        return cash, shares, cost_basis, 0.0

    cash -= actual_spend
    shares += qty
    cost_basis += actual_spend

    return cash, shares, cost_basis, actual_spend


def calc_metrics(equity_curve: pd.DataFrame, total_invested: float, trades: pd.DataFrame = None):
    equity = equity_curve["equity"]
    final_value = equity.iloc[-1]

    simple_return = final_value / total_invested - 1

    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    mdd = drawdown.min()

    days = (equity.index[-1] - equity.index[0]).days
    years = days / 365.25

    if years > 0 and total_invested > 0:
        cagr_simple = (final_value / total_invested) ** (1 / years) - 1
    else:
        cagr_simple = np.nan

    result = {
        "final_value": final_value,
        "total_invested": total_invested,
        "simple_return_pct": simple_return * 100,
        "cagr_simple_pct": cagr_simple * 100,
        "mdd_pct": mdd * 100,
    }

    if trades is not None and len(trades) > 0:
        result["trade_count"] = len(trades)
        result["win_rate_pct"] = (trades["pnl"] > 0).mean() * 100
        result["total_realized_pnl"] = trades["pnl"].sum()
    else:
        result["trade_count"] = 0
        result["win_rate_pct"] = np.nan
        result["total_realized_pnl"] = 0.0

    return result


# 전략 1: 매주 월요일 매수법

def backtest_monday_buy(df: pd.DataFrame):
    cash = INITIAL_CASH
    shares = 0.0
    cost_basis = 0.0

    total_invested = INITIAL_CASH
    rows = []

    for date, row in df.iterrows():
        price = float(row["Close"])

        # 월요일이면 추가입금 + 매수
        if date.weekday() == 0:
            if WEEKLY_CONTRIBUTION > 0:
                cash += WEEKLY_CONTRIBUTION
                total_invested += WEEKLY_CONTRIBUTION

            cash, shares, cost_basis, spent = buy_shares(
                cash=cash,
                shares=shares,
                cost_basis=cost_basis,
                price=price,
                amount=MONDAY_BUY_AMOUNT
            )

        equity = cash + shares * price

        rows.append({
            "date": date,
            "price": price,
            "cash": cash,
            "shares": shares,
            "cost_basis": cost_basis,
            "equity": equity
        })

    equity_curve = pd.DataFrame(rows).set_index("date")
    metrics = calc_metrics(equity_curve, total_invested)
    return equity_curve, metrics


# 전략 2: 라오어식 무한매수법
# 

def backtest_laor(df: pd.DataFrame):
    cash = INITIAL_CASH
    shares = 0.0
    cost_basis = 0.0

    total_invested = INITIAL_CASH

    cycle_unit = None
    buy_count = 0
    cycle_id = 1

    rows = []
    trades = []

    for date, row in df.iterrows():
        price = float(row["Close"])

        # 월요일 추가입금
        if date.weekday() == 0 and WEEKLY_CONTRIBUTION > 0:
            cash += WEEKLY_CONTRIBUTION
            total_invested += WEEKLY_CONTRIBUTION

        # 1) 목표수익률 도달 시 전량매도
        if shares > 0:
            avg_price = cost_basis / shares
            target_price = avg_price * (1 + LAOR_TAKE_PROFIT)

            if price >= target_price:
                gross_proceeds = shares * price
                pnl = gross_proceeds - cost_basis

                tax = max(pnl, 0) * TAX_RATE
                net_proceeds = gross_proceeds - tax

                cash += net_proceeds

                trades.append({
                    "sell_date": date,
                    "cycle_id": cycle_id,
                    "sell_price": price,
                    "avg_price": avg_price,
                    "shares": shares,
                    "gross_proceeds": gross_proceeds,
                    "pnl": pnl,
                    "tax": tax,
                    "net_proceeds": net_proceeds,
                    "buy_count": buy_count
                })

                shares = 0.0
                cost_basis = 0.0
                cycle_unit = None
                buy_count = 0
                cycle_id += 1

        # 2) 포지션이 없으면 새 사이클 시작
        if shares == 0 and cash > 0 and cycle_unit is None:
            cycle_unit = cash / LAOR_DIVISIONS
            buy_count = 0

        # 3) 라오어식 매일 1회 분할매수
        can_buy_more = True

        if LAOR_MAX_BUYS is not None:
            can_buy_more = buy_count < LAOR_MAX_BUYS

        if cash > 0 and cycle_unit is not None and can_buy_more:
            cash, shares, cost_basis, spent = buy_shares(
                cash=cash,
                shares=shares,
                cost_basis=cost_basis,
                price=price,
                amount=cycle_unit
            )

            if spent > 0:
                buy_count += 1

        equity = cash + shares * price

        rows.append({
            "date": date,
            "price": price,
            "cash": cash,
            "shares": shares,
            "cost_basis": cost_basis,
            "equity": equity,
            "cycle_id": cycle_id,
            "buy_count": buy_count
        })

    equity_curve = pd.DataFrame(rows).set_index("date")
    trades_df = pd.DataFrame(trades)

    metrics = calc_metrics(equity_curve, total_invested, trades_df)
    return equity_curve, trades_df, metrics


# 실행

def print_metrics(name: str, metrics: dict):
    print(f"\n[{name}]")
    print(f"최종 평가금액      : ${metrics['final_value']:,.2f}")
    print(f"총 투입금          : ${metrics['total_invested']:,.2f}")
    print(f"총 수익률          : {metrics['simple_return_pct']:,.2f}%")
    print(f"단순 CAGR          : {metrics['cagr_simple_pct']:,.2f}%")
    print(f"최대낙폭 MDD       : {metrics['mdd_pct']:,.2f}%")
    print(f"매도 횟수          : {metrics['trade_count']}")
    print(f"승률               : {metrics['win_rate_pct']:.2f}%" if not np.isnan(metrics["win_rate_pct"]) else "승률               : N/A")
    print(f"실현손익 합계      : ${metrics['total_realized_pnl']:,.2f}")


def main():
    df = load_price_data(TICKER, START_DATE, END_DATE)

    monday_curve, monday_metrics = backtest_monday_buy(df)
    laor_curve, laor_trades, laor_metrics = backtest_laor(df)

    print(f"\n백테스트 종목: {TICKER}")
    print(f"기간: {df.index[0].date()} ~ {df.index[-1].date()}")
    print(f"초기자금: ${INITIAL_CASH:,.2f}")
    print(f"매주 추가입금: ${WEEKLY_CONTRIBUTION:,.2f}")
    print(f"월요일 매수금액: ${MONDAY_BUY_AMOUNT:,.2f}")
    print(f"라오어 분할 수: {LAOR_DIVISIONS}")
    print(f"라오어 목표수익률: {LAOR_TAKE_PROFIT * 100:.1f}%")

    print_metrics("매주 월요일 매수법", monday_metrics)
    print_metrics("라오어식 무한매수법", laor_metrics)

    result = pd.DataFrame({
        "Monday_Buy": monday_curve["equity"],
        "Laor": laor_curve["equity"]
    })

    result["Monday_Drawdown"] = result["Monday_Buy"] / result["Monday_Buy"].cummax() - 1
    result["Laor_Drawdown"] = result["Laor"] / result["Laor"].cummax() - 1

    result.to_csv(f"{TICKER}_backtest_result.csv", encoding="utf-8-sig")

    if len(laor_trades) > 0:
        laor_trades.to_csv(f"{TICKER}_laor_trades.csv", index=False, encoding="utf-8-sig")

    # 평가금액 그래프
    plt.figure(figsize=(14, 7))
    plt.plot(result.index, result["Monday_Buy"], label="Monday Buy")
    plt.plot(result.index, result["Laor"], label="Laor Infinite Buy")
    plt.title(f"{TICKER} Backtest: Monday Buy vs Laor")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # MDD 그래프
    plt.figure(figsize=(14, 5))
    plt.plot(result.index, result["Monday_Drawdown"] * 100, label="Monday Buy MDD")
    plt.plot(result.index, result["Laor_Drawdown"] * 100, label="Laor MDD")
    plt.title(f"{TICKER} Drawdown Comparison")
    plt.xlabel("Date")
    plt.ylabel("Drawdown %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()