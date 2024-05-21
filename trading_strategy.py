import yfinance as yf
import pandas as pd
import numpy as np

# 데이터 다운로드
start_date = "2022-01-03"
end_date = "2024-05-17"
qqq = yf.download("QQQ", start=start_date, end=end_date)
tqqq = yf.download("TQQQ", start=start_date, end=end_date)

# 초기 조건 설정
initial_cash = 100000
cash = initial_cash
qqq_holdings = 0
tqqq_holdings = 0
qqq_avg_price = 0
tqqq_avg_price = 0

# 결과 저장용 DataFrame
results = []

# 이동평균선 계산
qqq['200ma'] = qqq['Close'].rolling(window=200).mean()

# 6개월(126 거래일) 및 4개월(84 거래일) 내 최고점 계산
qqq['6m_high'] = qqq['Close'].rolling(window=126).max()
qqq['4m_high'] = qqq['Close'].rolling(window=84).max()

# 매달 첫 거래일에 QQQ 1개 매수
qqq_monthly_purchase_days = qqq.resample('M').first().index

# 매도 금액 기록용 변수
last_sell_date = None

# 전략 적용
for date, row in qqq.iterrows():
    # 매달 첫 거래일에 QQQ 1개 매수
    if date in qqq_monthly_purchase_days and cash >= row['Close']:
        qqq_holdings += 1
        cash -= row['Close']
        qqq_avg_price = ((qqq_holdings - 1) * qqq_avg_price + row['Close']) / qqq_holdings

    # 매도 조건 체크 및 매수 조건 체크
    qqq_price = row['Close']
    tqqq_price = tqqq.loc[date, 'Close']
    
    # # 매도 조건을 충족한 후 2개월 동안 재적용 방지
    # if last_sell_date and (date - last_sell_date).days <= 60:
    #     continue

    # QQQ 매도 조건
    if qqq_price < row['200ma']:
        if qqq_price < row['6m_high'] * 0.9 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.2)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings
        
        if qqq_price < row['6m_high'] * 0.85 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.33)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings
        
        if qqq_price < row['6m_high'] * 0.8 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.5)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings
    
    if qqq_price >= row['200ma']:
        if qqq_price < row['4m_high'] * 0.95 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.3)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings
        
        if qqq_price < row['4m_high'] * 0.91 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.5)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date

            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings
            
        if qqq_price < row['4m_high'] * 0.895 and qqq_holdings > 0:
            sell_amount = int(qqq_holdings * 0.5)
            qqq_holdings -= sell_amount
            cash += sell_amount * qqq_price
            qqq_avg_price = (qqq_holdings * qqq_avg_price) / qqq_holdings if qqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 TQQQ 매수
            tqqq_buy_amount = int(cash // tqqq_price)
            if tqqq_buy_amount > 0:
                tqqq_holdings += tqqq_buy_amount
                cash -= tqqq_buy_amount * tqqq_price
                tqqq_avg_price = ((tqqq_holdings - tqqq_buy_amount) * tqqq_avg_price + tqqq_buy_amount * tqqq_price) / tqqq_holdings

    # TQQQ 매도 조건
    if tqqq_price > 0:
        tqqq_return = (tqqq_price - tqqq_avg_price) / tqqq_avg_price if tqqq_avg_price > 0 else 0
        if qqq_price < row['200ma'] and tqqq_return > 0.2 and tqqq_holdings > 0:
            sell_amount = int(tqqq_holdings * 0.33)
            tqqq_holdings -= sell_amount
            cash += sell_amount * tqqq_price
            tqqq_avg_price = (tqqq_holdings * tqqq_avg_price) / tqqq_holdings if tqqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 QQQ 매수
            qqq_buy_amount = int(cash // qqq_price)
            if qqq_buy_amount > 0:
                qqq_holdings += qqq_buy_amount
                cash -= qqq_buy_amount * qqq_price
                qqq_avg_price = ((qqq_holdings - qqq_buy_amount) * qqq_avg_price + qqq_buy_amount * qqq_price) / qqq_holdings
        
        if qqq_price < row['200ma'] and tqqq_return > 0.3 and tqqq_holdings > 0:
            sell_amount = int(tqqq_holdings * 0.5)
            tqqq_holdings -= sell_amount
            cash += sell_amount * tqqq_price
            tqqq_avg_price = (tqqq_holdings * tqqq_avg_price) / tqqq_holdings if tqqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 QQQ 매수
            qqq_buy_amount = int(cash // qqq_price)
            if qqq_buy_amount > 0:
                qqq_holdings += qqq_buy_amount
                cash -= qqq_buy_amount * qqq_price
                qqq_avg_price = ((qqq_holdings - qqq_buy_amount) * qqq_avg_price + qqq_buy_amount * qqq_price) / qqq_holdings
        
        if qqq_price >= row['200ma'] and tqqq_return > 0.2 and tqqq_holdings > 0:
            sell_amount = int(tqqq_holdings * 0.2)
            tqqq_holdings -= sell_amount
            cash += sell_amount * tqqq_price
            tqqq_avg_price = (tqqq_holdings * tqqq_avg_price) / tqqq_holdings if tqqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 QQQ 매수
            qqq_buy_amount = int(cash // qqq_price)
            if qqq_buy_amount > 0:
                qqq_holdings += qqq_buy_amount
                cash -= qqq_buy_amount * qqq_price
                qqq_avg_price = ((qqq_holdings - qqq_buy_amount) * qqq_avg_price + qqq_buy_amount * qqq_price) / qqq_holdings
        
        if qqq_price >= row['200ma'] and tqqq_return > 0.3 and tqqq_holdings > 0:
            sell_amount = int(tqqq_holdings * 0.5)
            tqqq_holdings -= sell_amount
            cash += sell_amount * tqqq_price
            tqqq_avg_price = (tqqq_holdings * tqqq_avg_price) / tqqq_holdings if tqqq_holdings > 0 else 0
            last_sell_date = date
            
            # 매도한 금액으로 QQQ 매수
            qqq_buy_amount = int(cash // qqq_price)
            if qqq_buy_amount > 0:
                qqq_holdings += qqq_buy_amount
                cash -= qqq_buy_amount * qqq_price
                qqq_avg_price = ((qqq_holdings - qqq_buy_amount) * qqq_avg_price + qqq_buy_amount * qqq_price) / qqq_holdings

        # 매수 조건 적용
        if cash > 5000 and (len(results) == 0 or (date - results[-1]['날짜']).days > 3):
            qqq_buy_amount = int(cash // qqq_price)
            if qqq_buy_amount > 0:
                qqq_holdings += qqq_buy_amount
                cash -= qqq_buy_amount * qqq_price
                qqq_avg_price = ((qqq_holdings - qqq_buy_amount) * qqq_avg_price + qqq_buy_amount * qqq_price) / qqq_holdings

    # 매매 기록 저장
    results.append({
        '날짜': date,
        'QQQ 매수량': 1 if date in qqq_monthly_purchase_days else 0,
        'QQQ 매도량': 0,  # 매도량은 위의 조건에 따라 추가 필요
        'QQQ 잔량': qqq_holdings,
        'QQQ 종가': qqq_price,
        'QQQ 매수 평균 가격': qqq_avg_price,
        'QQQ 종가치': qqq_holdings * qqq_price,
        'TQQQ 매수량': 0,  # 매수량은 매도 후 추가 필요
        'TQQQ 매도량': 0,  # 매도량은 매도 후 추가 필요
        'TQQQ 잔량': tqqq_holdings,
        'TQQQ 종가': tqqq_price,
        'TQQQ 매수 평균 가격': tqqq_avg_price,
        'TQQQ 종가치': tqqq_holdings * tqqq_price,
        '예수금': cash,
        '총 평가액': cash + (qqq_holdings * qqq_price) + (tqqq_holdings * tqqq_price)
    })

df_results = pd.DataFrame(results)

df_results.to_csv('stock_trading_simulation.csv', index=False, encoding='utf-8-sig')

print("시뮬레이션이 완료되었습니다. 결과가 ‘stock_trading_simulation.csv’ 파일로 저장되었습니다.")
