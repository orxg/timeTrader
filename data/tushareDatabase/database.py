# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:12:52 2017

@author: ldh

比较尴尬的点：
    1. pd.Timestamp对象不支持直接写入MySQL
    2. date,datetime是MySQL的关键字，不要当做列名
    3. 外键不能正常添加
"""

# database.py

from __future__ import print_function
import datetime as dt
import time

import pandas as pd
import pymysql
import tushare as ts

db_host = 'localhost'
db_user = 'sec_user'
db_pass = '123456'
db_name = 'securities' 

def update_tradedate_calendar():
    '''
    更新MySQL数据库中的交易日历。
    '''
    start_date = '1990-01-01'
    end_date = dt.date.today().strftime('%Y-%m-%d')
    tradedates = ts.get_k_data('000001',start = start_date,
                               end = end_date,
                               index = True)[['date']]
    
    tradedates.date = pd.to_datetime(tradedates.date)
    now = dt.date.today()
    tradedates['last_updated_time'] = now
    
    con = pymysql.connect(
            db_host,
            db_user,
            db_pass,
            db_name,
            charset = 'utf8')
    
    with con:
        tradedates.to_sql('tradedates',con,flavor = 'mysql',
                          if_exists = 'replace')
        
    print('成功更新交易日历数据tradedates')

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

def save_daily_price_pregened_from_tushare(data_tuple,con):
    '''
    根据股票代码代码与上市时间获得其前复权交易数据存储到数据库当中。
    
    Parameter
    ---------
        data_tuple:(ticker,timeToMarket,_id)
            ticker:股票代码
            timeToMarket:股票上市时间        
            _id:在数据库中的id
    '''
    ticker = data_tuple[0]
    timeToMarket = data_tuple[1]
    _id = data_tuple[2]
    
    timeToMarket = timeToMarket.strftime('%Y-%m-%d')
    today = dt.datetime.today().strftime('%Y-%m-%d')
    
    stock_data = ts.get_k_data(ticker,timeToMarket,today)
    stock_data.rename(columns = {
            'date':'date_time',
            'open':'open_price',
            'high':'high_price',
            'close':'close_price',
            'low':'low_price',
            'code':'ticker'},inplace = True)
    stock_data['stock_id'] = _id
    stock_data['last_updated_time'] = dt.datetime.today().strftime('%Y%m%d')
    
    
    daily_price = stock_data.values.tolist()    
    
    column_str = '''
    date_time,open_price,close_price,high_price,low_price,volume,
    ticker,stock_id,last_updated_time
    '''
    
    insert_str = ('%s,' * 9)[:-1]
    final_str = '''
    INSERT INTO daily_price (%s) VALUES (%s)
    '''%(column_str,insert_str)
    with con:
        cur = con.cursor()
        cur.executemany(final_str,daily_price)
    print('%s daily price was saved into the database successfully'%ticker)        
        
    
    

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
    SELECT ticker,timeToMarket,id FROM symbols;
    '''
    cur = con.cursor()
    cur.execute(sql_select_symbols)
    symbols = cur.fetchall()
    


    sql_create_table_schema = '''
    DROP TABLE IF EXISTS daily_price;
    CREATE TABLE  daily_price (
    id int not null primary key auto_increment,
    date_time datetime,
    open_price double,
    high_price double,
    low_price double,
    close_price double,
    volume double,
    ticker varchar(32),
    stock_id int not null,
    last_updated_time datetime,
    KEY idx_stock_id (stock_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''
    cur = con.cursor()
    cur.execute(sql_create_table_schema)
    
    print('Daily price table was successfully created')
    
    total_stock_num = len(symbols)
    for idx,symbol in enumerate(symbols):
        try:
            save_daily_price_pregened_from_tushare(symbol,con)
            print('%s \ %s'%(idx,total_stock_num))
        except Exception as e:
            print('%s was failed to save into the database !!!!!!'%symbol[0])
            print(e)
            print('%s \ %s'%(idx,total_stock_num))
        continue
    con.close()       
    
    

    
def initialize_financial_factors():
    '''
    初始化数据库中的财务数据。
    '''
    pass
    
if __name__ == '__main__':
#==============================================================================
#     initilize_daily_price_pregened()
#==============================================================================

