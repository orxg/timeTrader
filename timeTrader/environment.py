# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:32:38 2017

@author: LDH
"""

# environment.py
from .core.events import EventBus

class Environment():
    '''
    环境。
    '''
    _env = None
    
    def __init__(self,config):
        '''
        事件驱动的回测/模拟环境。
        
        Parameters
        ----------
        config
            回测环境设定。包括
                start_date:开始日期
                end_date:结束日期
                initial_cash:起始资金
                frequency:'1d',回测/模拟 类型
                rebalance_frequency:'5',调仓频率         
        '''
        Environment._env = self
        
        self.config = config # 用户定义
        

        self.envent_bus = EventBus()
        self.event_source = None
        self.universe = None
        self.portfolio = None
        self.context = None # 用户函数与Environment之间的接口
        self.data_proxy = None
        self.broker = None
        self.recorder = None
        
        self.start_date = None
        self.end_date = None
        self.canlendar = None
        self.calendar_datetime = None
        self.trading_datetime = None
        
        self.strategy_loader = None
        
        
    @classmethod
    def get_instance(cls):
        return Environment._env
        
    def set_event_source(self,event_source):
        self.event_source = event_source
        
    def set_universe(self,universe):
        self.universe = universe
        
    def set_context(self,context):
        self.context = context
        
    def set_data_proxy(self,data_proxy):
        self.data_proxy = data_proxy
        
    def set_broker(self,broker):
        self.broker = broker
        
    def set_portfolio(self,portfolio):
        self.portfolio = portfolio
        
    def set_recorder(self,recorder):
        self.recorder = recorder
        
    def set_calendar(self,calendar):
        self.calendar = calendar
        
    def set_strategy_loader(self,strategy_loader):
        self.strategy_loader = strategy_loader
        
if __name__ == '__main__':  
    config = {'base':{'start_date':'20150101',
              'end_date':'20160101',
              'initial_cash':100000,
              'frequency':'1d',
              'rebalance_frequency':'1'}}
    
    env = Environment(config)
    if env == Environment.get_instance():
        print('Successful')

    
    
        
