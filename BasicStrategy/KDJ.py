import sys
sys.path.append(r"/root/projects/quant")
import backtrader as bt
import matplotlib.pyplot as plt
import common.akdata as ds



''' 
策略说明:KDJ策略
计算方法：
RSV = （收盘价-N周期最低价)/(N周期最高价-N周期最低价)*100
K值 = RSV的N周期加权移动平均值
D值 = K值的N周期加权移动平均值
J值 = 3K-2D
一般来说，RSV的N周期选择9，K和D的N周期选择3。

当J值上穿K值的时候，是买入信号，此时买入。
当J值下穿K值的时候，是卖出信号，此时卖出。
'''


class S(bt.Strategy):
    # 初始化策略参数
    params = (
        ("period", 3),  # 最后一个","最好别删！
    )

    # 初始化函数
    def __init__(self):
        '''初始化属性、计算指标等'''
        self.dataclose=self.datas[0].close
        self.order=None
        self.buyprice=None
        self.buycomm=None
        
        self.highNine=bt.indicators.Highest(self.data.high,period=9)
        self.lowNine = bt.indicators.Lowest(self.data.low, period=9)
        self.rsv=100*bt.DivByZero(self.dataclose-self.lowNine,self.highNine-self.lowNine,zero=None)
        self.K=bt.indicators.EMA(self.rsv,period=3)
        self.D = bt.indicators.EMA(self.K, period=3)
        self.J = 3 * self.K - 2 * self.D
        pass

    def next(self):
        # 策略正常运行阶段，对应第min_period+1根bar-最后一根bar
        # 主要的策略逻辑都是写在该函数下
        # 进入该阶段后，会依次在每个bar上循环运行next函数
        self.log("Close, %.2f" % self.dataclose[0])
        if self.order:
            return
        
        if not self.position:
            # J - D 值
            condition1 = self.J[-1] - self.D[-1]
            condition2 = self.J[0] - self.D[0]
            if condition1 < 0 and condition2 > 0:
                self.log("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()

        else:
            if condition1 > 0 or condition2 < 0:
                self.log("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()
        pass

    # 日志打印：参考的官方文档
    def log(self, txt, dt=None, doprint=False):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        '''通知订单信息'''
        pass

    def notify_trade(self, trade):
        '''通知交易信息'''
        pass

    # 整个回测周期上，不同时间段对应的函数

    def start(self):
        '''在回测开始之前调用,对应第0根bar'''
        # 回测开始之前的有关处理逻辑可以写在这里
        # 默认调用空的 start() 函数，用于启动回测
        pass

    def prenext(self):
        '''策略准备阶段,对应第1根bar-第 min_period-1 根bar'''
        # 该函数主要用于等待指标计算，指标计算完成前都会默认调用prenext()空函数
        # min_period 就是 __init__ 中计算完成所有指标的第1个值所需的最小时间段
        pass

    def nextstart(self):
        '''策略正常运行的第一个时点，对应第 min_period 根bar'''
        # 只有在 __init__ 中所有指标都有值可用的情况下，才会开始运行策略
        # nextstart()只运行一次，主要用于告知后面可以开始启动 next() 了
        # nextstart()的默认实现是简单地调用next(),所以next中的策略逻辑从第 min_period根bar就已经开始执行
        pass

    def stop(self):
        '''策略结束，对应最后一根bar'''
        # 告知系统回测已完成，可以进行策略重置和回测结果整理了
        pass

    def notify_cashvalue(self, cash, value):
        '''通知当前资金和总资产'''
        pass

    def notify_fund(self, cash, value, fundvalue, shares):
        '''返回当前资金、总资产、基金价值、基金份额'''
        pass

    def notify_store(self, msg, *args, **kwargs):
        '''返回供应商发出的信息通知'''
        pass

    def notify_data(self, data, status, *args, **kwargs):
        '''返回数据相关的通知'''
        pass

    def notify_timer(self, timer, when, *args, **kwargs):
        pass
      #   返回定时器的通知
      # 定时器可以通过函数add_time()添加


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(S)

    # 添加数据
    cerebro.adddata(ds.SzStandardData(start_date="20230415"))

    # 资金管理
    cerebro.broker.setcash(100000)

    # 佣金设置
    cerebro.broker.setcommission(commission=0.005)

    # 交易数设置
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())

    cerebro.run(maxcpus=1)

    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='/root/projects/quant/result.png')
