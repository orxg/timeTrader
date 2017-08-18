# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:04:05 2017

@author: LDH
"""

# engines.py

# 环境
from environment import Environment

# 参与者与执行者
from .core.events import EVENT
from .core.broker import Broker
from .core.context import Context
from .core.portfolio import Portfolio
from .core.recorder import Recorder
from .core.executor import Executor
from .core.strategy import Strategy

# 模拟器与数据代理
from .mod.simulation_event_source import SimulationEventSource
from .data_proxy.tushareDatabase.data import TushareMySQLDataProxy

# utils
from .utils.strategy_loader import StrategyLoader
from .utils.base_scope import create_base_scope

class SimulationEngine():
    '''
    回测引擎。
    '''
    def __init__(self,config):
        self.config = config
    
    def _run_simulation(self,source_code):
        '''
        Parameters:
            source_code
                用户策略源代码
        '''
        # 基本组件
        env = Environment(self.config)
        
        env.set_broker(Broker())
        env.set_context(Context())
        env.set_portfolio(Portfolio())
        env.set_recorder(Recorder())
        
        env.set_event_source(SimulationEventSource())
        env.set_data_proxy(TushareMySQLDataProxy())
        
        env.set_universe(self.config.base.universe)
        env.start_date,env.end_date = self.config.base.start_date,self.config.base.end_date
        
        calendar = env.data_proxy.get_calendar(env.start_date,env.end_date)
        env.set_calendar(calendar)
        
        env.set_strategy_loader(StrategyLoader())
        
        # 对策略源代码进行编译
        scope = create_base_scope() # 创建用户代码的namespace
        user_strategy = Strategy(env.event_bus,scope,env.context)
        
        # 执行在env环境下的回测
        Executor(env).run()
        
    def run(self,source_code):
        self._run_simulation(source_code)

