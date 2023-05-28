import sys
sys.path.append(r"/root/projects/quant")

import backtrader as bt
import matplotlib.pyplot as plt
import common.akdata as ds

class MyStrategy(bt.Strategy):
    def __init__(self):
        print("init")

    def next(self):
        print('当前可用资金', self.broker.getcash())

    def log(self, txt, dt=None, do_print=False):
        print(self.datas[0].datetime.date(0))


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)

    # 添加数据
    cerebro.adddata(ds.SzStandardData(start_date="20230415"))

    # 资金管理
    cerebro.broker.setcash(1000000)
    
    # 
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    
    # 设置滑点
    # 百分比
    # 方式1：通过 BackBroker 类中的 slip_perc 参数设置百分比滑点
    cerebro.broker = bt.brokers.BackBroker(slip_perc=0.0001)
    # 方式2：通过调用 brokers 的 set_slippage_perc 方法设置百分比滑点
    cerebro.broker.set_slippage_perc(perc=0.0001)
    # 固定
    # 方式1：通过 BackBroker 类中的 slip_fixed 参数设置固定滑点
    cerebro.broker = bt.brokers.BackBroker(slip_fixed=0.001)
    # 方式2：通过调用 brokers 的 set_slippage_fixed 方法设置固定滑点
    cerebro.broker.set_slippage_fixed(fixed=0.001)


    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())
    cerebro.run(maxcpus=1)
    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='./test.png')
