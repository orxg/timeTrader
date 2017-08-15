# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:14:32 2017

@author: LDH

回测所需交易数据准备。
"""

# backtest_data_initilizer.py

from collections import defaultdict

import pandas as pd

from data.tushareDatabase.data import TushareMySQLDataProvider
from tradedate_calendar.tradedate_calendar import TradeDateCalendar

data_provider = TushareMySQLDataProvider()

class BacktestDataInitilizer():
    '''
    初始化回测所需要的数据，提供给回测、context、blotter使用。
    在回测中，仅提供get_history_data方法作为一切回测中可能用到的数据的数据接口。
    '''
    def __init__(self,universe,start_date,end_date):
        '''
        初始化数据对象。
        Parameters
        -----------
            universe:股票池
            start_date:开始日期
            end_date：结束日期
        '''
        self.universe = universe
        self.start_date = start_date
        self.end_date = end_date
        self.calendar = TradeDateCalendar()
        self.calendar_list = self.calendar.get_tradedates_list(
        self.start_date,
        self.end_date)
        
        self._history_data = {} # 存储所有历史数据
        self._historic_data_generator = {} # 股票数据生成器
        
        self._current_date_data = {} # 当前数据
        self._available_historic_data = defaultdict(pd.DataFrame) # 可获得数据
        
        self._prepare_data()
        
    def _prepare_data(self):
        '''
        准备数据。按ticker进行存储。
        '''
        for stock_ticker in self.universe:
            trade_data = data_provider.get_daily_price(stock_ticker,
                                                       self.start_date,
                                                       self.end_date)
            trade_data = trade_data.set_index('date_time')
            trade_data = trade_data.reindex(self.calendar_list)
            trade_data = trade_data.fillna(method = 'pad')
            self._history_data[stock_ticker] = trade_data

        self._initilize_historic_data_generator() # 初始化股票历史数据生成器
        
    def _initilize_historic_data_generator(self):
        '''
        股票历史数据生成器。
        '''
        for ticker in self.universe:
            stock_data = self._history_data[ticker]
            stock_data = stock_data.iterrows()
            self._historic_data_generator[ticker] = stock_data

        
    def get_history_data(self):
        '''
        提供历史数据。
        '''
        pass
    
    @property
    def current_date_data(self):
        '''
        回测当前交易日的数据。
        暴露该接口给blotter进行撮合判定。
        暴露该接口给context进行账户更新判定。
        '''
        
        return self._current_date_data
    
    @property
    def available_historic_data(self):
        '''
        回测当前可获得的数据。
        '''
        return self._available_historic_data
    
    def refresh_data(self):
        '''
        更新当前交易日的数据以及目前可获得的历史数据。
        '''
        # 更新可获得的数据
        for ticker in self.universe:
            try:
                current_data = self._current_date_data[ticker][1]
                self._available_historic_data[ticker] = self._available_historic_data[ticker].append(current_data)
            except:
                break # 说明尚未开始回测
        
        # 更新当前交易日的数据
        for ticker in self.universe:
            self._current_date_data[ticker] = next(
                    self._historic_data_generator[ticker])

    
if __name__ == '__main__':
    data_test = BacktestDataInitilizer(['600340'],'20150101','20160101')

    
    

