# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:39:05 2017

@author: LDH

交易记录对象。
"""

# recorder.py
import matplotlib.pyplot as plt

class Recorder():
    '''
    交易状况记录、统计。
    '''
    def __init__(self):
        '''
        初始化。
        '''
        self.portfolio_pnl = []
        self.historic_position = []
        self.historic_market_value = []
    
    def record_context(self,portfolio_value):
        '''
        记录当前账户状况。
        '''
        self.portfolio_pnl.append(portfolio_value)
        
    def plot_pnl(self):
        '''
        做出曲线
        '''
        plt.plot(self.portfolio_pnl)
        plt.grid()
        
if __name__ == '__main__':
    record = Recorder()
    
        
        

