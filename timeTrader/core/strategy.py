# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:08:52 2017

@author: LDH
"""

# strategy.py
from events import EVENT

class Strategy():
    '''
    负责向环境中event_bus中添加策略监听函数，传递context。
    '''
    def __init__(self,event_bus,scope,context):
        self.context = context
        self.event_bus = event_bus
        
        self._initilize = scope.get('initilize',None)
        self._handle_bar = scope.get('handle_bar',None)
        self._before_trading = scope.get('before_trading',None)
        self._after_trading = scope.get('after_trading',None)
        
        self.event_bus.add_listener(EVENT.POST_SYSTEM_INIT,self.initilize)
        self.event_bus.add_listener(EVENT.BAR,self.handle_bar)
        self.event_bus.add_listener(EVENT.BEFORE_TRADING,self.before_trading)
        self.event_bus.add_listener(EVENT.POST_TRADING,self.after_trading)
        
    def initilize(self,event):
        self._initilize(self.context)
        
    def handle_bar(self,event):
        self._handle_bar(self.context)
        
    def before_trading(self,event):
        self._before_trading(self.context)
        
    def after_trading(self,event):
        self._after_trading(self.context)


