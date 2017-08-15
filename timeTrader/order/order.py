# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 16:49:20 2017

@author: LDH

订单对象。
"""

# order.py

class Order():
    '''
    订单对象。
    '''
    def __init__(self,ticker,direction,amount,order_price):
        '''
        订单对象初始化。
        Parameters
        ------------
            ticker
                股票代码  
            direction
                方向  
            amount
                数量，如300股  
            order_price
                下单价格  
        '''
        self.ticker = ticker
        self.direction = direction
        self.amount = amount
        self.order_price = order_price
        
    
class FillOrder():
    '''
    成交反馈。

    '''
    def __init__(self,ticker,direction,amount,fill_price,commision):
        '''
        成交反馈对象初始化。
        Parameters
        -----------
            ticker
                股票代码
            direction
                方向
            amount
                成交数量，如300股
            fill_price
                成交价格
            commision
                手续费
        '''
        self.ticker = ticker
        self.direction = direction
        self.amount = amount
        self.fill_price = fill_price
        self.commision = commision
        
    