import backtrader as bt
import matplotlib.pyplot as plt
import data.akdata as ds


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma1=bt.indicators.MovingAverageSimple(period=3)
        self.ema1=bt.indicators.ExponentialMovingAverage(self.datas[0], period=3)
        self.close_over_sma=self.data.close>self.sma1
        self.close_over_ema=self.data.close>self.ema1
        self.sma_ema_diff=self.sma1-self.ema1
        # self.buy_sig=bt.And(self.close_over_ema,self.close_over_sma,self.sma_ema_diff>0)
        
        self.sma5=bt.indicators.MovingAverageSimple(period=5)
        self.sma10=bt.indicators.MovingAverageSimple(period=10)
        self.buy_sig=self.sma5>self.sma10
        
        
        
        
        
    def next(self):
        print('datetime', self.datas[0].datetime.date(0))
        # 打印当日、昨日、前日的均线
        print('sma1',self.sma1.get(ago=0, size=3))
        # if self.buy_sig:
        #     self.buy()
        
    def log(self,txt,dt=None,do_print=False):
        print(self.datas[0].datetime.date(0))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    # # 获取数据
    # stock_hfq_df = ak.stock_zh_a_hist(
    #     symbol="002373", adjust="hfq", start_date="20190115", end_date="20230523").iloc[:, :6]
    # stock_hfq_df.columns = [
    #     'date',
    #     'open',
    #     'close',
    #     'high',
    #     'low',
    #     'volume',
    # ]
    # stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    # startDate = datetime(2020, 5, 11)
    # endDate = datetime(2023, 5, 23)
    # data = bt.feeds.PandasData(
    #     dataname=stock_hfq_df, fromdate=startDate, todate=endDate)
    
    data=ds.SzStandardData()

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
    
    
