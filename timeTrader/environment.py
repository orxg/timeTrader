# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:32:38 2017

@author: LDH
"""

# environment.py

class Environment():
    '''
    环境。
    '''
    _environment = None
    
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
        Environment._environment = self
        self.config = config
        self.envent_bus = None
        self.event_source = None
        self._universe = None
        self.context = None
        self.data_proxy = None
        self.blotter = None
        self.record = None
        self.canlendar = None
        self.calendar_datetime = None
        self.trading_datetime = None
        
    @classmethod
    def get_instance(cls):
        return Environment._environment
    
    def set_event_bus(self,event_bus):
        self.event_bus = event_bus
        
    def set_event_source(self,event_source):
        self.event_source = event_source
        
    def set_universe(self,universe):
        self._universe = universe
        
    def set_context(self,context):
        self.context = context
        
    def set_data_proxy(self,data_proxy):
        self.data_proxy = data_proxy
        
    def set_blotter(self,blotter):
        self.blotter = blotter
        
    def set_recorder(self,recorder):
        self.recorder = recorder
        
    def set_calendar(self,calendar):
        self.calendar = calendar
        
if __name__ == '__main__':
    env = Environment()
    if env == Environment.get_instance():
        print('Successful')
    
    config = {'start_date':'20150101',
              'end_date':'20160101',
              'initial_cash':100000,
              'frequency':'1d',
              'rebalance_frequency':'1'}
    
    
        
