import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import common.akdata as ds
import backtrader as bt


'''
第四步在第三步基础上开始向建立一个简单的回测逻辑，包含买卖逻辑。
逻辑说明如下：
买入：连续两天下跌，即当天收盘价小于昨日收盘价，昨日收盘价小于前日收盘价
卖出：连续两天上涨，即当天收盘价大于昨日收盘价，昨日收盘价大于前日收盘价
该逻辑没有实际意义，实际策略请看BasicStrategy文件夹。
回测数据为002373：220415-230415的数据。运行代码，可以看到根据该策略，最终资金为87404。
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
        # 若连续两天下跌，则买入
        if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
            self.log("买入， 价格为： %.2f" % self.dataclose[0])
            self.buy()
        elif self.dataclose[0] > self.dataclose[-1] and self.dataclose[-1] > self.dataclose[-2]:
            self.log("卖出， 价格为： %.2f" % self.dataclose[0])
            self.sell()

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

    # 加载数据,添加了002373(千方科技)从2022年4月15日到2023年4月15日的数据
    cerebro.adddata(ds.SzStandardData(
        code="002373", start_date="20210415", end_date="20230415"))

    # 添加策略
    cerebro.addstrategy(TestStrategy)

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())
