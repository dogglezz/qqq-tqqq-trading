import yfinance as yf
import pandas as pd
import numpy as np

# 데이터 다운로드
start_date = "2022-01-03"
end_date = "2024-05-17"
qqq = yf.download("QQQ", start=start_date, end=end_date)
tqqq = yf.download("TQQQ", start=start_date, end=end_date)
