### bt交易流程
1. 设置初始交易条件：初始资金、交易税费、滑点、成交量限制等；
2. 完善策略逻辑中交易指令 buy、sell、close，或取消交易 cancel
3. Order 模块会解读交易订单，进一步由经纪商 Broker 模块处理
4. 经纪商 Broker 会根据订单信息检查订单并确定是否接收订单，在接收后会按订单要求撮合成交 trade，并进行成交结算；
5. Order 模块返回经纪商 Broker 中的订单执行结果。 

### 交易费用设置
1. commission：手续费 / 佣金；
2. mult：乘数；
3. margin：保证金 / 保证金比率 。
4. 双边征收：买入和卖出操作都要收取相同的交易费用 。

对于交易订单生成和执行时间，Backtrader 默认是 "当日收盘后下单，次日以开盘价成交"

### 下单函数
Strategy 中的常规下单函数主要有 3 个：买入 buy() 、卖出 sell()、平仓 close() 

通过 cancel() 来取消订单 ：self.cancel(order)；

### 交易状态
1. Order.Created：订单已被创建；
2. Order.Submitted：订单已被传递给经纪商 Broker；
3. Order.Accepted：订单已被经纪商接收；
4. Order.Partial：订单已被部分成交；
5. Order.Complete：订单已成交；
6. Order.Rejected：订单已被经纪商拒绝；
7. Order.Margin：执行该订单需要追加保证金，并且先前接受的订单已从系统中删除；
8. Order.Cancelled (or Order.Canceled)：确认订单已经被撤销；
9. Order.Expired：订单已到期，其已经从系统中删除 。    


Strategy 中的 __init__() 函数在回测过程中只会在最开始的时候调用一次，而 next() 会每个交易日依次循环调用多次。

调用 Indicators 模块的函数计算指标时，默认是对 self.datas 数据对象中的第一张表格中的第一条line （默认第一条line是 close line）计算相关指标。

        # bt.And 中所有条件都满足时返回 1；有一个条件不满足就返回 0
        self.And = bt.And(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Or 中有一个条件满足时就返回 1；所有条件都不满足时返回 0
        self.Or = bt.Or(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.If(a, b, c) 如果满足条件 a，就返回 b，否则返回 c
        self.If = bt.If(self.data>self.sma5,1000, 5000)
        # bt.All,同 bt.And
        self.All = bt.All(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Any，同 bt.Or
        self.Any = bt.Any(self.data>self.sma5, self.data>self.sma10, self.sma5>self.sma10)
        # bt.Max，返回同一时刻所有指标中的最大值
        self.Max = bt.Max(self.data, self.sma10, self.sma5)
        # bt.Min，返回同一时刻所有指标中的最小值
        self.Min = bt.Min(self.data, self.sma10, self.sma5)
        # bt.Sum，对同一时刻所有指标进行求和
        self.Sum = bt.Sum(self.data, self.sma10, self.sma5)
        # bt.Cmp(a,b), 如果 a>b ，返回 1；否则返回 -1
        self.Cmp = bt.Cmp(self.data, self.sma5)