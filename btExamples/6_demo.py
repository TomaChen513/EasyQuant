import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import common.akdata as ds
import backtrader as bt



'''
demo案例展示
策略说明：
买入：收盘价上涨突破20日均线
卖出：收盘价跌破20日均线
结果可以看出，通过观察均线的策略比5所展示的简单策略要成功。
'''

class TestStrategy(bt.Strategy):
    # 策略参数，可以在导入策略时修改用于寻优
    params = (("maperiod",20),)
    
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
        
        # 20日均线
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

    # 每次执行回测时执行的函数
    def next(self):
        # 每次回测时输出每日收盘价
        # self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        
        if not self.position:
            if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
                self.order = self.buy(size=100)  # 执行买入
                self.log("买入，价格为： %.2f , 当前持仓：%d" %
                     (self.dataclose[0], self.getposition().size))
        else:
            if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
                self.order = self.sell(size=100)  # 执行卖出
                self.log("卖出，价格为： %.2f , 当前持仓：%d" %
                     (self.dataclose[0], self.getposition().size))
                

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
                self.log(
                    f"买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
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
    # cerebro.optstrategy(TestStrategy, maperiod=range(3, 10))  # 导入策略参数寻优,运行这个时无法plot

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())
    
    # 绘图
    # 此行代码经过修改backtrader源码，会在本文件夹下保存结果图片。目的是可以在服务器上保存图片以供查看。未修改源码运行则会报错。
    cerebro.plot(style='candlestick', fileName=os.path.dirname(os.path.abspath(__file__)) + "/result.png")
    # 正常运行选择这个
    # cerebro.plot(style='candlestick')
