import backtrader as bt
import matplotlib.pyplot as plt
import data.akdata as ds


class MyStrategy(bt.Strategy):
    def __init__(self):
        
    def next(self):
        
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