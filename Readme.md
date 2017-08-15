# 介绍
个人量化研究环境。

# 约定
## 命名规则
模块名/文件名: event,signal_sender
方法/函数: get_data  
类名: HistoryDataHandler  
对象: historyDataHandler  
常量: CONSTANT_VARIABLE  
变量: this_is_a_variable  

## 文档格式
'''
功能说明。

Parameter
---------
....

Return
---------
....

'''

## data数据结构

# 架构
实现BacktestEngine,根据策略编写其initilize方法与handle_data方法。BacktestEngine实例化对象实现start_backtest方法对回测进行封装。

backtest_data_initilizer
	根据指定参数，初始化回测所需的交易数据。为回测提供数据接口。
context
	共享backtest_data_initilizer的数据接口,与blotter进行交互。提供查询、下单、接收交易反馈的功能。
blotter
	共享backtest_data_initilizer的数据接口,与context进行交互。提供根据交易数据进行撮合的功能，提供下单指令反馈，停牌判定。其共享数据提前context一个交易日(日间)。
recorder
	对账户状况进行记录,对交易效果进行统计。
order
	该对象提供对订单的描述。

## 主目录  

## 模块
### data
#### tushareDatabase
提供基于tushare的数据库创建、维护、提取等功能的接口。数据库默认为MySQL.

### strategy  

### calendar定义交易日期
calendar:提供交易日历  


### out
#### bt
保存回测结果 
 
#### live
保存live结果  

### log
日志。


# 更新日志
## 2017-08-15
进度:
1. 完成了基于tushare的本地数据库搭建(股票基本信息、日前复权数据)
2. 完成了大体的回测架构,使用buy_and_hold策略进行了测试，结果与优矿基本一致。

下一步的计划：
1. 程序细节的增加与优化(策略回测统计结果、手续费精确化、涨停跌停判定、考虑滑点的影响、增加更多的order类型、停牌判定)
2. 整体程序api的优化(优化各模块的功能与交互、加强易用性和可扩展性)
3. 建立因子数据库(基于tushare)、增加日数据更新函数、增加因子数据库的更新函数、建立分钟线数据库
4. 加入模拟交易的功能(基于tushare实时行情,加入日志功能与信号发送功能)

# 所需软件
1. python2.7(Anaconda)
2. pymysql
3. tushare

## 说明
