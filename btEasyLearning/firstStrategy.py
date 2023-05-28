import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class SmaStrategy(bt.Strategy):
    params = (("maperiod",3),)

    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    def log(self,txt,dt=None,do_print=False):
        print(self.datas[0].datetime.date(0))
            
    # 主逻辑
    def next(self):
        self.log(self.data_close[0])
        self.log("123")
        if self.order:  # 检查是否有指令等待执行,
            return
        # 检查是否持仓
        if not self.position:  # 没有持仓
            if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                
                self.order = self.buy(size=100)  # 执行买入
        else:
            if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell(size=100)  # 执行卖出
                
    def stop(self):
        self.log("(MA均线： %2d日) 期末总资金 %.2f" % (self.params.maperiod, self.broker.getvalue()), do_print=True)
        return super().stop()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaStrategy)
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
