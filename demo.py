import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class MyStrategy(bt.Strategy):
    def __init__(self):
        
        
    def next(self):
        
    def log(self,txt,dt=None,do_print=False):
        print(self.datas[0].datetime.date(0))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    # 获取数据
    stock_hfq_df = ak.stock_zh_a_hist(
        symbol="002373", adjust="hfq", start_date="20190115", end_date="20230523").iloc[:, :6]
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    startDate = datetime(2023, 5, 11)
    endDate = datetime(2023, 5, 23)
    data = bt.feeds.PandasData(
        dataname=stock_hfq_df, fromdate=startDate, todate=endDate)
    
    print(stock_hfq_df)

    # 初始设置
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='./test.png')
