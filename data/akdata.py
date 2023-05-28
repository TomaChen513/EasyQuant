import akshare as ak
import backtrader as bt
from datetime import datetime
import pandas as pd


def SzStandardData(code="002373",adjust="hfq",start_date="20190115",end_date="20230523"):
    # 获取数据
    stockDf = ak.stock_zh_a_hist(symbol=code, adjust=adjust, start_date=start_date, end_date=end_date).iloc[:, :6]
    # 标准化成bt输入数据格式
    stockDf.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 索引修改为date
    stockDf.index = pd.to_datetime(stockDf['date'])
    startDate = _parseDateTime(start_date)
    endDate = _parseDateTime(end_date)
    stockData = bt.feeds.PandasData(dataname=stockDf, fromdate=startDate, todate=endDate)
    return stockData

# 字符串解析成datetime格式
def _parseDateTime(date):
    year=int(date[:4])
    month=int(date[4:6])
    day=int(date[6:])
    return datetime(year=year,month=month,day=day)
    