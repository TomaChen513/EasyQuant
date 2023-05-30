import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import common.akdata as ds
import backtrader as bt



'''
第四步我们的策略成功运行了，但是我们并不知道其中的过程,因此也就无法根据结果调整我们的策略，因此第五步我们需要在第四步的基础上展示策略交易的过程。
从两方面展示:
1. log输出
2. 图像显示
回测数据为002373：220415-230415的数据。
'''


class TestStrategy(bt.Strategy):
    # 回测初始化时函数，在一整个回测周期只会执行一次
    def __init__(self):
        # 设置dataclose为第一个数据集的收盘价
        self.dataclose = self.datas[0].close

        # 设置order来记录订单情况
        self.order = None
        # 设置buyprice来记录购买价格
        self.buyprice = None
        # 设置佣金来展示购买时刻的佣金
        self.buycomm = None

    # 每次执行回测时执行的函数
    def next(self):
        # 每次回测时输出每日收盘价
        # self.log('Close, %.2f' % self.dataclose[0])
        # 若连续两天下跌，则买入
        if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2]:
            self.log("买入，价格为： %.2f , 当前持仓：%d" %
                     (self.dataclose[0], self.getposition().size))
            self.buy()
        elif self.dataclose[0] > self.dataclose[-1] and self.dataclose[-1] > self.dataclose[-2]:
            self.log("卖出，价格为： %.2f , 当前持仓：%d" %
                     (self.dataclose[0], self.getposition().size))
            self.sell()

    # 用来输出日志，下面书写格式参考官方日志写法
    def log(self, txt, dt=None):
        # 当dt为空时默认输出为回测时间点，不为空时输出为dt
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # 用来打印订单信息
    def notify_order(self, order):
        # 若订单已被传递给经纪商或被接收
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 若订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)
        # 若因异常原因拒绝
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单异常! Canceled/Margin/Rejected')

        # 清空order状态
        self.order = None

    # 用来打印交易信息
    def notify_trade(self, trade):
        # 若交易还在进行
        if not trade.isclosed:
            return

        # 显示交易的利润(毛利润：税前利润，净利润：税后利润)
        self.log('操作利润, 毛利润 %.2f, 净利润 %.2f' % (trade.pnl, trade.pnlcomm))


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
    
    # 绘图
    # 此行代码经过修改backtrader源码，会在本文件夹下保存结果图片。目的是可以在服务器上保存图片以供查看。未修改源码运行则会报错。
    cerebro.plot(style='candlestick', fileName=os.path.dirname(os.path.abspath(__file__)) + "/result.png")
    # 正常运行选择这个
    # cerebro.plot(style='candlestick')