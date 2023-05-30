import backtrader as bt

'''
backtrader的初始化，通常用来设置量化交易的本金、佣金、滑点等，下面是一个简单示例。
'''
if __name__ == '__main__':
    # 初始化cerebro
    cerebro = bt.Cerebro()
    # 设置本金
    cerebro.broker.setcash(10000)
    # 设置百分比佣金，单位是百分数
    cerebro.broker.setcommission(commission=0.005)
    # 设置百分比滑点
    cerebro.broker.set_slippage_perc(perc=0.0001)

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())
