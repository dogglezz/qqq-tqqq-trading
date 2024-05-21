import yfinance as yf
import pandas as pd
import numpy as np

# 현재 날짜 설정
today = pd.Timestamp.today().strftime('%Y-%m-%d')

# 데이터 다운로드
start_date = "2022-05-01"
end_date = today
qqq = yf.download("QQQ", start=start_date, end=end_date)
tqqq = yf.download("TQQQ", start=start_date, end=end_date)

# 이동평균선 계산
qqq['200ma'] = qqq['Close'].rolling(window=200).mean()

# 6개월(126 거래일) 및 4개월(84 거래일) 내 최고점 계산
qqq['6m_high'] = qqq['Close'].rolling(window=126).max()
qqq['4m_high'] = qqq['Close'].rolling(window=84).max()

# 현재 QQQ와 TQQQ의 가격 및 지표
qqq_price = qqq.iloc[-1]['Close']
tqqq_price = tqqq.iloc[-1]['Close']
qqq_200ma = qqq.iloc[-1]['200ma']
qqq_6m_high = qqq.iloc[-1]['6m_high']
qqq_4m_high = qqq.iloc[-1]['4m_high']

# 매매 전략 적용
def decide_what_to_buy(qqq_price, tqqq_price, qqq_200ma, qqq_6m_high, qqq_4m_high):
    decision = ""
    
    # QQQ 매수 조건
    if qqq_price < qqq_200ma:
        if qqq_price < qqq_6m_high * 0.9:
            decision = "Buy TQQQ"
        elif qqq_price < qqq_6m_high * 0.85:
            decision = "Buy TQQQ"
        elif qqq_price < qqq_6m_high * 0.8:
            decision = "Buy TQQQ"
    elif qqq_price >= qqq_200ma:
        if qqq_price < qqq_4m_high * 0.95:
            decision = "Buy TQQQ"
        elif qqq_price < qqq_4m_high * 0.91:
            decision = "Buy TQQQ"
        elif qqq_price < qqq_4m_high * 0.895:
            decision = "Buy TQQQ"
    
    # TQQQ 매수 조건
    if qqq_price >= qqq_200ma and decision == "":
        decision = "Buy QQQ"
    elif qqq_price < qqq_200ma and decision == "":
        decision = "Buy QQQ"

    return decision

# 현재 시점에서 매수 결정을 내림
decision = decide_what_to_buy(qqq_price, tqqq_price, qqq_200ma, qqq_6m_high, qqq_4m_high)
print(f"At the current time, it is recommended to: {decision}")
