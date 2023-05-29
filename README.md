## Introduction(Continuously Updating~)
本项目是一个量化策略集合，对常用的策略进行建模回测。主要使用的工具有backtrader和akshare。backtrader用于建立回测模型，akshare则是获得开源的公开数据。下面是所使用工具的简单介绍：
### backtrader
Backtrader是一个基于Python的自动化回溯测试框架，作者是德国人 Daniel Rodriguez，是一个易懂、易上手的量化投资框架。

文档：https://www.backtrader.com/docu/
### AKShare
AKShare 是基于 Python 的财经数据接口库，目的是实现对股票、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据从数据采集、数据清洗到数据落地的一套工具，主要用于学术研究目的。

文档：https://akshare.akfamily.xyz/

### 项目架构
* 基本策略集合：BasicStrategy
* backtrader学习教程： btExamples
* backtrader整合akshare输入流库：common

### 如何部署
建议安装conda虚拟环境，在虚拟环境中按照官方教程安装backtrader和akshare即可运行～

## Reference
* backtrader文档：https://www.backtrader.com/docu/

* akshare文档：https://akshare.akfamily.xyz/

* backtrader指标查看文档：https://www.backtrader.com/docu/indautoref/

* TA-Lib：https://www.ta-lib.org/

* 入门学习资料：https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNTc0Mjg0Mg==&action=getalbum&album_id=2380299870701420545&scene=173&from_msgid=2653316888&from_itemidx=1&count=3&nolastread=1#wechat_redirect

## Future Work
* Alphalens教程
* 强化学习于量化交易的应用