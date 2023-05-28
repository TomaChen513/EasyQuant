import sys
sys.path.append(r"/root/projects/quant")
import backtrader as bt
import common.akdata as ds



# 策略说明
# 买入： 五日价格移动平均线(MA5)和十日价格移动平均线(MA10)形成均线金叉（MA5上穿MA10）原理：最近处于涨势
# 卖出： 五日价格移动平均线(MA5)和十日价格移动平均线(MA10)形成均线死叉（MA10下穿MA5）原理：最近处于跌势


class AverageGoldenDeadFork(bt.Strategy):
    # 初始化策略参数
    params = (
        ("period5", 5),
        ("period10", 10),
    )

    # 初始化函数
    def __init__(self):
        '''初始化属性、计算指标等'''
        # 初始化数据
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # sma5 and sma10
        self.sma5 = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.period5)
        self.sma10 = bt.indicators.MovingAverageSimple(
            self.datas[0], period=self.params.period10)

    def next(self):
        # 记录收盘价
        self.log("CLose: %.2f" % self.dataclose[0])

        # 判断是否为订单状态，只能允许一个订单存在
        if self.order:
            return

        # 判断是否买入
        if not self.position:
            # 未买，且SMA5>SMA10，买入
            if self.sma5[0] > self.sma10[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0], doprint=True)
                self.order = self.buy()
        else:
            # 已经买了，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0], doprint=True)
                self.order = self.sell()

    def log(self, txt, dt=None, doprint=False):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    # 打印回测日志

    def notify_order(self, order):
        '''通知订单信息'''
        if order.status in [order.Submitted, order.Accepted]:
            # 若已传递给broker
            return

        # 若订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)
        # 若因异常原因拒绝
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        '''通知交易信息'''
        if not trade.isclosed:
            return

        # 显示交易的毛利率和净利润
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), doprint=True)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(AverageGoldenDeadFork)

    # 添加数据
    cerebro.adddata(ds.SzStandardData(start_date="20190415"))

    # 资金管理
    cerebro.broker.setcash(10000)

    # 佣金设置
    cerebro.broker.setcommission(commission=0.005)

    # 交易股票数设置，固定数
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())

    cerebro.run(maxcpus=1)

    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='./test.png')
