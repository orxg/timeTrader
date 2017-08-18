# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 14:41:30 2017

@author: LDH

"""

# events.py

from enum import Enum
from collections import defaultdict

class Event():
    def __init__(self,event_type,**kwargs):
        self.event_type = event_type
        self.__dict__ = kwargs
        
    def __repr__(self):
        return ' '.join('{}:{}'.format(k, v) for k, v in self.__dict__.items())
    
class EventBus():
    def __init__(self):
        self._listeners = defaultdict(list)
        
    def add_listener(self,event,listener):
        self._listeners[event].append(listener)
        
    def prepend_listener(self,event,listener):
        self._listeners[event].insert(0,listener)
        
    def publish_event(self,event):
        for listener in self._listeners[event.event_type]:
            # 监听者处理事件,若返回True,则停止
            if listener(event): 
                break
            
class EVENT(Enum):
    
    # 系统启动前的初始化
    POST_SYSTEM_INIT = 'post_system_init'
    
    # 交易前
    BEFORE_TRADING = 'before_trading'
    
    # BAR事件,传递的却是一个截面的数据：如日间回测传递的是当日的所有universe中的股票交易数据
    BAR = 'bar'
    
    # 交易后
    POST_TRADING = 'post_trading'
    

    
        