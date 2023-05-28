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
        
        print('close', self.data.close[0], self.data.close)
        print('sma5', self.sma5[0], self.sma5)
        print('sma10', self.sma10[0], self.sma10)
        print('buy_sig', self.buy_sig[0], self.buy_sig)
        if self.data.close > self.sma5:
            print('------收盘价上穿5日均线------')
        if self.data.close[0] > self.sma10:
            print('------收盘价上穿10日均线------')
        if self.buy_sig:
            print('------ buy ------')
        
    def log(self,txt,dt=None,do_print=False):
        print(self.datas[0].datetime.date(0))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)

    # 初始设置
    cerebro.adddata(ds.SzStandardData(start_date="20230415"))
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='./test.png')
    
    
