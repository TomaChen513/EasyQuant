import akshare as ak
import backtrader as bt
from datetime import datetime
import pandas as pd
import time


def _getDataFromCsv(code,start_date,end_date):
    stockData=pd.read_csv('/root/projects/quant/common/'+code+'.csv',parse_dates=['日期']).iloc[:, :6]
    stockData.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 索引修改为date
    stockData.index = pd.to_datetime(stockData['date'])
    print(stockData)
    data = bt.feeds.PandasData(
        dataname=stockData, fromdate="20210415", todate=end_date)
    
    return data


def SzStandardData(code="002373", adjust="hfq", start_date="10230115", end_date="20240523"):
    # 检查是否存在数据
    stockData=_getDataFromCsv(code=code,start_date=start_date,end_date=end_date)
    if stockData is not None:
        return stockData

    print("go to api")
    # 从api获取数据
    stockDf = ak.stock_zh_a_hist(
        symbol=code, adjust=adjust, start_date=start_date, end_date=end_date).iloc[:, :6]
    # 标准化成bt输入数据格式
    stockDf.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    stockDf[0]=datetime.strptime(stockDf[0],"%Y-%m-%d")
    # 索引修改为date
    stockDf.index = pd.to_datetime(stockDf['date'])
    startDate = _parseDateTime(start_date)
    endDate = _parseDateTime(end_date)
    stockData = bt.feeds.PandasData(
        dataname=stockDf, fromdate=startDate, todate=endDate)
    print(stockDf)
    return stockData

# 字符串解析成datetime格式
def _parseDateTime(date):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])
    return datetime(year=year, month=month, day=day)

# 获得股票列表
def _getAllCnStock():
    stock_info = ak.stock_info_a_code_name()
    stock_codes = stock_info["code"].tolist()
    return stock_codes
    
# 获得所有股票数据
def getAllCnStock():
    codeList=_getAllCnStock()
    
    adjust="hfq"
    start_date="10230115"
    end_date=datetime.now().strftime("%Y%m%d")
    for code in codeList:
        stockDf = ak.stock_zh_a_hist(symbol=code, adjust=adjust, start_date=start_date, end_date=end_date)
        stockDf.to_csv(''+code+'.csv',index=False)
        time.sleep(5)
        
