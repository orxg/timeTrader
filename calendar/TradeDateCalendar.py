# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 13:40:13 2017

@author: LDH

"""

# TradeDateCalendar.py

import datetime as dt

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

sql = '''
SELECT date from tradedates
'''
with con:
    dates = pd.read_sql(sql,con,parse_dates = ['date'])['date']

class TradeDateCalendar():
    
    def __init__(self):
        '''
        初始化交易日历。
        '''
        self.tradedates = dates
        
    def move_n_tradedays(self,date,n = 1):
        '''
        获得date向前n日的交易日期。
        
        Parameter
        -----------
            date: datetime对象或str
            n : float
            
        Return
        -------
            pandas.Timestamp对象
        '''
        if isinstance(date,str):
            date = dt.datetime.strptime(date,'%Y%m%d')

        idx = self.tradedates[self.tradedates == date].index[0]
        
        idx = idx + n
        moved_date = self.tradedates.iloc[idx]
        return moved_date
    
    def get_tradedates_list(self,start_date,end_date):
        '''
        返回指定时间段内内交易日的list.
        
        Parameters
        ----------
            start_date:开始,'20160101',支持datetime
            end_date:结束,'20170101',支持datetime
            
        Return
        --------
            交易日的list.每个对象为pandas.Timestamp
        '''
        
        tradedates_series = self.tradedates[(self.tradedates >= start_date) & (self.tradedates <= end_date)]
        tradedates_list = tradedates_series.tolist()
        return tradedates_list
        

if __name__ == '__main__':
    CAL = TradeDateCalendar()
    

