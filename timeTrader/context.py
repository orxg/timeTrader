# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:50:07 2017

@author: LDH

账户对象。
"""

# context.py

from order.order import Order
from position import Position

class Context():
    '''
    账户对象。
    '''
    def __init__(self,cash,universe,blotter,data_provider):
        '''
        初始化一个账户。目前支持初始为空仓。
        '''
        self.cash = cash
        self.universe = universe
        self.blotter = blotter
        self.data_provider = data_provider
        self._position = Position(self.universe)
        
        self._market_value = {}
        self._total_market_value = 0
        self._portfolio_value = self.cash + self._total_market_value
        
        for ticker in self.universe:
            self._market_value[ticker] = 0
        
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
        return self._portfolio_value
    
    @property
    def position(self):
        '''
        提供当前资产的持仓状况。
        '''
        return self._position
    
    def order(self,ticker,direction,amount):
        '''
        下单函数.向blotter中添加order对象。目前默认按照开盘价下单。
        
        Parameters
        ----------
            ticker
                股票代码
            direction
                方向
            amount
                数量，如300股
        '''
        order_price = self.data_provider.current_date_data[ticker][1]['open_price']
        
        if direction == 1:
            if order_price * amount < self.cash:
                order = Order(ticker,direction,amount,order_price)
                self.blotter.current_orders_universe.append(order)
            else:
                pass
            
        if direction == -1:
            if self.position.position[ticker] >= amount:
                order = Order(ticker,direction,amount,order_price)
                self.blotter.current_orders_universe.append(order)
            else:
                pass
            
        
    def refresh_account_from_match_result(self):
        '''
        根据撮合结果更新账户。
        '''
        if len(self.blotter.current_fillorders_universe) == 0:
            return 0
        print('here7')
        for each in self.blotter.current_fillorders_universe:
            ticker = each.ticker
            direction = each.direction
            print('here11')
            amount = each.amount
            print('here10')
            fill_price = each.fill_price
            print('here9')
            commision = each.commision
            print('here8')
            self.cash += - direction * (fill_price * amount) - commision
            self._position.refresh_position(ticker,direction,amount)
            print('here4')
        self.blotter.current_fillorders_universe = []
        
        
    def refresh_account_from_market(self):
        '''
        根据最新的市场信息更新账户。
        '''
        current_date_data = self.data_provider.current_date_data
        
        self._total_market_value = 0
        for ticker,amount in self._position.position.items():
            ticker_close_price = current_date_data[ticker][1]['close_price']
            self._market_value[ticker] = ticker_close_price * amount
            self._total_market_value += self._market_value[ticker]
            
        self._portfolio_value = self._total_market_value + self.cash
            
            
    
    
if __name__ == '__main__':
    pass
