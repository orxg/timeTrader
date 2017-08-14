# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:50:07 2017

@author: LDH

账户对象。
"""

# context_lib.py

from order import Order

class Context():
    '''
    账户对象。
    '''
    def __init__(self,cash,blotter,position = None):
        '''
        初始化一个账户。目前支持初始为空仓。
        '''
        self.cash = cash
        self.position = position
        self.capital = self.cash
        self.blotter = blotter
        
    @property
    def previous_date(self):
        '''
        提供回测中前一个交易日的交易日期。
        '''
        pass
    
    @property
    def portfolio_value(self):
        '''
        提供当前资产组合的总价值。
        '''
        pass
    
    @property
    def position(self):
        '''
        提供当前资产的持仓状况。
        '''
        pass
    
    def order(self):
        '''
        下单函数.向blotter中添加order对象。
        '''
        order = Order()
        pass
    
if __name__ == '__main__':
    pass
