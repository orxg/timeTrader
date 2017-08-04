# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:12:52 2017

@author: ldh
"""

# database.py

import tushare as ts
import pymysql
import datetime as dt

db_host = 'localhost'
db_user = 'sec_user'
db_pass = '123456'
db_name = 'securities' 

def date_time_str_convertor(date):
    try:
        time_to_market = dt.datetime.strptime(str(date),'%Y%m%d')
        return time_to_market
    except:
        return dt.datetime(1991,1,1)
    
def get_symbols_save_into_db(mode = 'replace'):
    '''
    获取股票基本信息存入数据库.
    
    Parameters
    -----------
        mode
            模式,replace创建新表,append在原表上添加。
    '''
    now = dt.datetime.now()
    
    data = ts.get_stock_basics()

    con = pymysql.connect(
            host = db_host,
            user = db_user,
            passwd = db_pass,
            db = db_name,
            charset = 'utf8')
    
    data['created_time'] = now
    data['last_updated_time'] = now
    data['id'] = range(1,len(data) + 1)
    data['ticker'] = data.index
    data['timeToMarket'] = data['timeToMarket'].apply(date_time_str_convertor)
    data.to_sql('symbols',con,if_exists = 'replace',
                index = False,flavor = 'mysql')
    
    sql = '''
    ALTER TABLE symbols
    ADD PRIMARY KEY (id);
    '''
    
    cur = con.cursor()
    cur.execute(sql)
    con.close()
    print('成功更新symbols表(股票基本信息)')

def initilize_daily_price_pregened():
    '''
    初始化数据库前复权数据。
    
    '''
    con = pymysql.connect(
            host = db_host,
            user = db_user,
            passwd = db_pass,
            db = db_name,
            charset = 'utf8')
    
    sql_select_symbols = '''
    SELECT ticker,timeToMarket FROM symbols;
    '''
    cur = con.cursor()
    cur.execute(sql_select_symbols)
    symbols = cur.fetchall()
    
    return symbols
    for ticker,time_to_market in symbols:
        ticker_data = ts.get_k_data(ticker)
    
if __name__ == '__main__':
#==============================================================================
#     get_symbols_save_into_db()
#==============================================================================
    symbols = initilize_daily_price_pregened()

