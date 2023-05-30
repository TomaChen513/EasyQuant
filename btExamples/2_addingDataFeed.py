import backtrader as bt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import common.akdata as ds



'''
在新建完backtrader的大脑后，我们需要确定回测的数据来源。backtrader支持多种数据来源，在这里使用的是akshare的数据，并在common.akdata中进行了封装以满足backtrader的格式要求。下面是在1的基础上进行的一个简单数据载入示例。
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

    # 加载数据,添加了002373(千方科技)从2022年4月15日到2023年4月15日的数据
    cerebro.adddata(ds.SzStandardData(code="002373",start_date="20220415", end_date="20230415"))

    print('起始本金: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('回测最终资金: %.2f' % cerebro.broker.getvalue())