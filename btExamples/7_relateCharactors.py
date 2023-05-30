import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import backtrader as bt
import common.akdata as ds



'''
这一部分展示常用的指标和逻辑
'''


class TestStrategy(bt.Strategy):
    # 策略参数，可以在导入策略时修改用于寻优
    params = (("maperiod", 20),)

    # 回测初始化时函数，在一整个回测周期只会执行一次
    def __init__(self):
        self.sma1 = bt.indicators.MovingAverageSimple(
            period=self.params.maperiod)
        self.ema1 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=self.params.maperiod)

    # 每次执行回测时执行的函数
    def next(self):
        print('当前可用资金', self.broker.getcash())
        print('当前总资产', self.broker.getvalue())
        print('当前持仓量', self.broker.getposition(self.data).size)
        print('当前持仓成本', self.broker.getposition(self.data).price)

    # 用来输出日志，下面书写格式参考官方日志写法

    def log(self, txt, dt=None):
        # 当dt为空时默认输出为回测时间点，不为空时输出为dt
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


if __name__ == '__main__':
    # 初始化cerebro
    cerebro = bt.Cerebro()
    # 设置本金
    cerebro.broker.setcash(100000)
    # 设置百分比佣金，单位是百分数
    cerebro.broker.setcommission(commission=0.005)
    # 设置百分比滑点
    cerebro.broker.set_slippage_perc(perc=0.0001)
    # 交易数设置
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

    # 加载数据,添加了002373(千方科技)从2022年4月15日到2023年4月15日的数据
    cerebro.adddata(ds.SzStandardData(
        code="002373", start_date="20210415", end_date="20230415"))

    # 添加策略
    cerebro.addstrategy(TestStrategy)
    # cerebro.optstrategy(TestStrategy, maperiod=range(3, 10))  # 导入策略参数寻优,运行这个时无法plot

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())