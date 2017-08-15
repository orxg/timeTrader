# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:37:32 2017

@author: FSB
"""

# test.py

from base import BacktestEngine

if __name__ == '__main__':
    class buy_and_hold(BacktestEngine):
        def handle_data(self):
            self.context.order('600340',1,100)
            
    easy_test = buy_and_hold(['600340'],'20160101','20170101')