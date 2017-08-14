# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:41:40 2017

@author: LDH
撮合器。
"""

# blotter.py

def Blotter():
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

    def match(self):
        '''
        撮合。
        '''
        pass

    
