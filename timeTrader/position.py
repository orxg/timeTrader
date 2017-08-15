# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 09:11:22 2017

@author: LDH
"""

# position.py

class Position():
    '''
    持仓对象。
    '''
    def __init__(self,universe):
        '''
        初始化。
        '''
        self.universe = universe
        self.position = {} # key为ticker，value为持仓股票数量
        
        for ticker in self.universe:
            self.position[ticker] = 0
            
    def refresh_position(self,ticker,direction,amount):
        '''
        更新持仓。
        '''
        self.position[ticker] += direction * amount
    
        
        

