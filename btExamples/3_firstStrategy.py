import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import common.akdata as ds
import backtrader as bt



'''
第三步开始向建立的cerebro添加策略，这是通过继承bt的Strategy类实现的。接下来会展示建立逻辑所需要的必要框架。
'''


class TestStrategy(bt.Strategy):
    # 回测初始化时函数，在一整个回测周期只会执行一次
    def __init__(self):
        # 设置dataclose为第一个数据集的收盘价
        self.dataclose = self.datas[0].close

    # 每次执行回测时执行的函数
    def next(self):
        # 每次回测时输出每日收盘价
        self.log('Close, %.2f' % self.dataclose[0])

    # 用来输出日志，下面书写格式参考官方日志写法
    def log(self, txt, dt=None):
        # 当dt为空时默认输出为回测时间点，不为空时输出为dt
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


if __name__ == '__main__':
    # 初始化cerebro
    cerebro = bt.Cerebro()
    # 设置本金
    cerebro.broker.setcash(10000)
    # 设置百分比佣金，单位是百分数
    cerebro.broker.setcommission(commission=0.005)
    # 设置百分比滑点
    cerebro.broker.set_slippage_perc(perc=0.0001)
    # 交易数设置
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 加载数据,添加了002373(千方科技)从2022年4月15日到2023年4月15日的数据
    cerebro.adddata(ds.SzStandardData(
        code="002373", start_date="20220415", end_date="20230415"))

    # 添加策略
    cerebro.addstrategy(TestStrategy)

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())
