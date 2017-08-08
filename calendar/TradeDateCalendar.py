# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 13:40:13 2017

@author: LDH

"""

# TradeDateCalendar.py

import pandas as pd
import pymysql

db_host = 'localhost'
db_user = 'sec_user'
db_pass = '123456'
db_name = 'securities' 

con = pymysql.connect(
        host = db_host,
        user = db_user,
        passwd = db_pass,
        db = db_name,
        charset = 'utf8')
#==============================================================================
# con = create_engine('mysql://{user}:{pws}@{host}/{db}'.format(
#         user = db_user,
#         pws = db_pass,
#         host = db_host,
#         db = db_name),charset = 'utf8')
#==============================================================================

sql = '''
SELECT date from tradedates
'''
with con:
    dates = pd.read_sql(sql,con,parse_dates = ['date'])[['date']]

class TradeDateCalendar():
    
    def __init__(self):
        '''
        初始化交易日历。
        '''
        self.tradedates = dates
        
    def forward(self,date,n = 1):
        '''
        获得date向前n日的交易日期。
        
        Parameter
        -----------
            date: datetime对象
            n : float
            
        Return
        -------
            datetime对象
        '''
        
        pass
    
    def back(self,date,n = 1):
        '''
        获得date向后n日的交易日期。
        
        Parameter
        -----------
            date: datetime对象
            n : float
            
        Return
        -------
            datetime对象
        '''
    pass

if __name__ == '__main__':
    pass

