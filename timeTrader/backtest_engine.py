# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:05:20 2017

@author: LDH

顶层。
封装回测、模拟交易的逻辑。

"""

# backtest_engine.py

from __future__ import print_function
from abc import abstractmethod

from context import Context
from blotter import Blotter
from backtest_data_initilizer import BacktestDataInitilizer
from recorder import Recorder


class BacktestEngine():
    '''
    回测引擎。
    '''
    
    def __init__(self,universe,start_date,end_date,
                 cash = 100000,
                 trading_frequency = 'd',
                 rebalance_frequency = '1'):
        '''
        初始化回测设定。
        
        Parameters
        -----------
            universe:股票池
            start_date:开始日期,%Y%m%d
            end_date：结束日期,%Y%m%d
            trading_frequency:交易频率，默认为日间
            rebalance_frequency:调仓频率，默认为1
            
        '''
        self.universe = universe
        self.start_date = start_date
        self.end_date = end_date
        self.cash = cash
        self.trading_frequency = 'd'
        self.rebalance_frequency = '1'
        
        self._construct_backtest_environment()
    
    @abstractmethod
    def initilize(self):
        '''
        策略初始化。
        '''
        pass
    
    @abstractmethod
    def handle_data(self):
        '''
        策略函数。
        提供self.context,self.data接口。
        self.context提供下单函数order.
        self.data提供历史数据函数get_history_data.
        '''
        pass
    
    def _construct_backtest_environment(self):
        '''
        初始化回测环境。
        '''

        
        self.data = BacktestDataInitilizer(
                self.universe,
                self.start_date,
                self.end_date)
        
        self.blotter = Blotter(self.data)
        self.context = Context(self.cash,
                               self.universe,
                               self.blotter,
                               self.data) 
        self.recorder = Recorder()

        
    def _run_backtest(self):
        '''
        回测。
        '''
        # 获取交易日历
        trading_calendar = self.data.calendar_list
        
 
        
        # 进行回测
        self.initilize()
        for tradeDate in trading_calendar:
            self.data.refresh_data() # 更新data对象在当前交易日所能获得的数据以及当前交易日的数据
            print('here1')
            self.handle_data() # 执行交易逻辑,向blotter中添加订单
            print('here2')
            self.blotter.match() # 执行撮合
            print('here3')
            self.context.refresh_account_from_match_result() # 根据撮合结果更新账户
            print('here4')
            self.context.refresh_account_from_market() # 根据市场状况更新账户
            print('here5')
            self.recorder.record_context(self.context.portfolio_value) # 记录当前的账户的状况
            print('here6')
        print('The backtest is over.')
        
    def start_backtest(self):
        '''
        进行回测。
        '''
        self._run_backtest()
           

if __name__ == '__main__':
    class buy_and_hold(BacktestEngine):
        def handle_data(self):
            self.context.order('600340',1,100)
            
    easy_test = buy_and_hold(['600340'],'20160101','20170101')





