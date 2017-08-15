# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:41:40 2017

@author: LDH
撮合器。
"""

# blotter.py

from order.order import Order,FillOrder

class Blotter():
    '''
    提供撮合功能。
    '''
    def __init__(self,data_provider):
        '''
        撮合器，记录订单信息，根据data_provider提供的接口进行成交判定，
        反馈成交结果。
        '''
        self.data_provider = data_provider
        self.current_orders_universe = [] # 当前所有订单信息
        self.current_fillorders_universe = [] # 当前所有反馈信息

    def match(self):
        '''
        撮合。默认按照开盘价撮合成交。
        
        Retrun
        -------
            若无下单，
                则返回None,不更新current_fillorders_universe
            若有下单，
                则返回list,元素为FillOrder对象
        '''      
        for each in self.current_orders_universe:
            ticker = each.ticker
            direction = each.direction
            amount = each.amount
            order_price = each.order_price
            
            maximum_volume = self.data_provider.current_date_data[ticker][1]['volume']
            
            # 成交量判定,小于当日成交量1/10则可以成交
            if amount * 10 < maximum_volume:
                match_price = order_price # 此处目前为开盘价
                commision = 5 # 此处目前为默认手续费
                fillorder = FillOrder(ticker,direction,amount,match_price,commision)
                self.current_fillorders_universe.append(fillorder)
            else:
                match_price = order_price # 此处目前为开盘价
                commision = 5 # 此处目前为默认手续费
                fillorder = FillOrder(ticker,direction,
                                      int(maximum_volume / 10/100)*100,
                                      match_price,
                                      commision)
                self.current_fillorders_universe.append(fillorder)
                
        self.current_orders_universe = []
        
if __name__ == '__main__':
    pass
    
