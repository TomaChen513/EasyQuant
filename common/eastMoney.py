import backtrader as bt

'''
东方财富的交易规则示例。
规则如下：
东方财富股票交易手续费包括佣金、印花税和过户费。
佣金:万2.5，单笔最少5元。
印花税:卖出时收取成交金额的千分之1，买入不收。
过户费:成交金额的万分之0.2，买卖双向收取。如果买卖金额不足5元，则按5元收取。 
'''
# Todo: 待测试


class EastMoneyCommission(bt.CommInfoBase):
    params = (
        ("commission", 0.00025),  # 佣金，万2.5
        ("stampDuty", 0.001),  # 印花税
        ("transferFee", 0.00002),  # 过户费
        ("stocklike", True),
    )

    def _getcommission(self, size, price, pseudoexec):
        totalCommission = abs(size)*price*self.params.commission
        totaltransferFee = abs(size)*price*self.params.transferFee
        totalstampDuty = abs(size)*price*self.params.stampDuty
        # 买入
        if size > 0:
            if totalCommission < 5:
                totalCommission = 5
            if totaltransferFee < 5:
                totaltransferFee = 5
            return totaltransferFee+totalCommission
        # 卖出
        elif size < 0:
            if totalCommission < 5:
                totalCommission = 5
            if totaltransferFee < 5:
                totaltransferFee = 5
            return totalCommission+totalstampDuty+totaltransferFee
        else:
            return 0


def _testEastMoneyCommission():
    cerebro = bt.Cerebro()
    comminfo = EastMoneyCommission()
    cerebro.broker.addcommissioninfo(comminfo)
