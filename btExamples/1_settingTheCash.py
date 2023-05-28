from datetime import datetime

import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    cerebro=bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())