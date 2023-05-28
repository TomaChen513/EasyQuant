import sys
sys.path.append(r"/root/projects/quant")

import backtrader as bt
import matplotlib.pyplot as plt
import common.akdata as ds

# 策略说明
# 买入： 五日价格移动平均线(MA5)和十日价格移动平均线(MA10)形成均线金叉（MA5上穿MA10）原理：最近处于涨势
# 卖出： 五日价格移动平均线(MA5)和十日价格移动平均线(MA10)形成均线死叉（MA10下穿MA5）原理：最近处于跌势



class AverageGoldenDeadFork(bt.Strategy):
    # 初始化策略参数
    params = (
        ("period",3), # 最后一个","最好别删！
    )
    
    # 初始化函数
    def __init__(self):
        '''初始化属性、计算指标等'''
        # 指标计算可参考《backtrader指标篇》
        pass
    
    
    def next(self):
        # 策略正常运行阶段，对应第min_period+1根bar-最后一根bar
        # 主要的策略逻辑都是写在该函数下
        # 进入该阶段后，会依次在每个bar上循环运行next函数
        pass


    # 日志打印：参考的官方文档
    def log(self, txt, dt=None,doprint=False):
        '''构建策略打印日志的函数：可用于打印订单记录或交易记录等'''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))
  

    
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
    
  # 打印回测日志
    def notify_order(self, order):
        '''通知订单信息'''
        pass

    def notify_trade(self, trade):
        '''通知交易信息'''
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
    cerebro.addstrategy(AverageGoldenDeadFork)

    # 添加数据
    cerebro.adddata(ds.SzStandardData(start_date="20230415"))

    # 资金管理
    cerebro.broker.setcash(100000)
    
    # 佣金设置
    cerebro.broker.setcommission(commission=0.005)
    
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


    # 运行
    print("期初总资金： %.2f" % cerebro.broker.getvalue())
    
    cerebro.run(maxcpus=1)
    
    print("期末总资金: %.2f" % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style='candlestick', fileName='./test.png')
