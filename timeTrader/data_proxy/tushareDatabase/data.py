# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 10:09:51 2017

@author: LDH
"""
import pymysql 
import pandas as pd

class TushareMySQLDataProxy():
    '''
    MySQL中通过Tushare获取的数据库的api.
    '''
    def __init__(self):
        '''
        初始化。默认直接开启。
        '''
        self.host = 'localhost'
        self.user = 'sec_user'
        self.passwd = '123456'
        self.db = 'securities'
        
        self.start() # 开启接口
        
    def start(self):
        '''
        开启接口。
        '''
        self.con = pymysql.connect(
                self.host,
                self.user,
                self.passwd,
                self.db)
               
    def close(self):
        '''
        关闭接口。
        '''
        self.con.close()
        
    def get_daily_price(self,ticker,start_date,end_date):
        '''
        获取日间交易数据。
        
        Parameter
        ---------
            ticker:股票代码
            start_date:开始日期 %Y%m%d
            end_date:结束日期 %Y%m%d
        
        Return
        --------
            DataFrame
        '''
        
        sql = '''
        SELECT dp.date_time,dp.open_price,
        dp.high_price,dp.low_price,dp.close_price,
        dp.volume
        FROM daily_price as dp 
        INNER JOIN symbols as s
        ON dp.stock_id = s.id
        WHERE s.ticker = {ticker}
        AND dp.date_time >= {start_date}
        AND dp.date_time <= {end_date}
        '''.format(ticker = ticker,
        start_date = start_date,
        end_date = end_date)
        
        daily_price_df = pd.read_sql(sql,self.con,parse_dates = ['date_time'])
        return daily_price_df
	
	def get_calendar(self, start_date,end_date):
		'''
		获取交易日历的list.
		'''
		sql = 
		'''
		SELECT date from tradedates
		'''
		dates = pd.read_sql(sql,con,parse_dates = ['date'])['date']
		return dates[start_date:end_date].tolist()
		
if __name__ == '__main__':
    dataProvider = TushareMySQLDataProvider()
    df = dataProvider.get_daily_price('600340','20060101','20160131')
    dataProvider.close()
    
    