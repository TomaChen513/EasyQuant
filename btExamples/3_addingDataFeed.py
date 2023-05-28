from datetime import datetime

import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd

def dataSource(code="002373"):
    stock_hfq_df = ak.stock_zh_a_hist(
        symbol=code, adjust="hfq", start_date='20230515', end_date='20230519').iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    start_date = datetime(2023, 5, 20)  # 回测开始时间
    end_date = datetime(2023, 5, 23)  # 回测结束时间
    data = bt.feeds.PandasData(
        dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 规范化数据格式
    # print(stock_hfq_df)
    return data
    

if __name__ == '__main__':
    cerebro=bt.Cerebro()
    
    # set cash
    cerebro.broker.setcash(100000.0)
    
    # add data
    cerebro.adddata(dataSource())
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())