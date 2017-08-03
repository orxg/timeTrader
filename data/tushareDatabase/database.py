# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 16:12:52 2017

@author: ldh
"""

# database.py

import tushare as ts
from sqlalchemy import create_engine,String
import datetime as dt

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
    
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = '3228864'
    db_name = 'securities'
    
    
    con = create_engine('mysql://{user}:{pws}@{server}/{db}'.format(
            user = db_user,
            pws = db_pass,
            server = db_host,
            db = db_name))
    
    data['created_time'] = now
    data['last_updated_time'] = now
    data['id'] = range(1,len(data) + 1)

    
    # 此处有问题，在python3上无法实现
    # 明天去Python2环境下试一下，打算写sql语句实现
    data.to_sql('symbols',con,if_exists = 'replace',
                index = False,
                dtype = {'name':String(32),
                         'industry':String(32),
                         'area':String(32)})
    
    sql = '''
    ALTER TABLE symbols
    ADD PRIMARY KEY (id);
    '''
    
    cur = con.cursor()
    cur.execute(sql)
    con.close()
    print('成功更新symbols表(股票基本信息)')
    


    
if __name__ == '__main__':
    data = get_symbols_save_into_db()
    

