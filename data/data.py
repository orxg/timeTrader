# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 16:01:30 2017

@author: LDH
数据接口。
"""
# data.py

from abc import ABCMeta
import datetime as dt

import pandas as pd
import pymssql as ms
import tushare as ts

class AbstractDataProvider:
    '''
    抽象数据提供类。
    '''
    __metaclass__ = ABCMeta
    
    
class GuosenSQLServer(AbstractDataProvider):
    '''
    基于国信证券本地数据库的数据接口。既可以作为研究所用的数据接口，也可以用于回测。
    '''
    
    def __init__(self,backtest = True,
                 events_queue = None,
                 universe = None,
                 start_date = None,
                 end_date = None):
        '''
        初始化数据接口。
        
        Parameters
        ----------
            backtest
                是否为回测所需。默认为True,表示用于策略回测。否则不提供回测方法。
            events_queue
                回测事件队列。若backtest为True,events_queue必须不为None,否则会报错。
            universe
                回测股票池
            start_date
                回测开始日期
            end_date
                回测结束日期
        '''
        if backtest is True:
            if events_queue is None:
                raise ValueError('events_queue is not given')
                
        self.backtest = backtest
        self.events_queue = events_queue
        self.universe = universe
        self.start_date = start_date
        self.end_date = end_date
        
        if backtest is True:
            self.backtest_calendar = self._get_backtest_calendar()
            self._backtest_data = {}
            # self._prepare_backtest_data()
            
    
    def get_daily_data(self,ticker,start_date,end_date):
        '''
        获取单只股票日数据。此函数无法正常运行。
        
        Parameters
        -----------
            ticker
                股票代码,'600340'
            start_date
                开始日期,'20170801'
            end_date
                结束日期,'20170803'
        Return
        -------
            pandas.DataFrame
                index
                    datetime
                columns
                    ['open_price','high_price','low_price','close_price',
                    'volume','adj_pre_close_price']
        Notes
        ------
            由于联合查询效率很低，加入时间限制后分开查询再利用pandas合并。
            如果数据库能够把这些数据进行整合，效率会提高。受制于当前数据库。
            目前仍有问题。前复权因子无法正常获取。
        '''
        server = '172.19.62.183'
        user = 'DataAdmin'
        passwd = 'fs95536!'
        db = 'BasicData'
    
        
        start_date_num = dt.datetime.strptime(start_date,'%Y%m%d').toordinal() + 366
        end_date_num = dt.datetime.strptime(end_date,'%Y%m%d').toordinal() + 366
        
        print start_date_num
        print end_date_num
        sql_open = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_DayOpen] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)
        
        sql_high = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_DayHigh] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)
        
        sql_low = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_DayLow] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)
        
        sql_close = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_DayClose] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)  
        
        sql_volume = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_DayVol] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)   
        
        sql_recoveredGene = '''
        SELECT numtime,
        value
        FROM [BasicData].[dbo].[Yi_RecoveredGene] 
        WHERE stockcode = %s
        AND numtime >= %s
        AND numtime <= %s
        '''%(ticker,start_date_num,end_date_num)         
        con = ms.connect(
            server,user,passwd,db)

        with con:
            data_open = pd.read_sql(sql_open,con).rename(columns = {'value':'open_price'})
            data_high = pd.read_sql(sql_high,con).rename(columns = {'value':'high_price'})
            data_low = pd.read_sql(sql_low,con).rename(columns = {'value':'low_price'})
            data_close = pd.read_sql(sql_close,con).rename(columns = {'value':'close_price'})
            data_volume = pd.read_sql(sql_volume,con).rename(columns = {'value':'volume'})
            data_recoveredGene = pd.read_sql(sql_recoveredGene,con).rename(columns = {'value':'recoveredGene'})
            data_list = [data_open,data_high,
                         data_low,data_close,
                         data_volume,data_recoveredGene]
        data = pd.concat(data_list,join_axes = ['numtime'])
        data['datetime'] = data['numtime'].apply(lambda x: dt.datetime.fromordinal(x) - 366)
        latest_recovered_gene = data.iloc[-1]['recoveredGene']
        data['adj_pre_close_price'] = data['close'] * data['recoveredGene'] / latest_recovered_gene
        data.drop(['numtime','recoveredGene'],inplace = True)
        data.set_index('datetime',inplace = True)
        
        return data

    
    def get_universe_daily_data(self,universe,start_date,end_date):
        '''
        获取多只股票日数据。
        '''
        pass
    
    def get_factor_data(self):
        '''
        获取因子数据。暂不实现。
        '''
        pass      
    
    def _get_backtest_calendar(self):
        '''
        获取交易日历。
        目前日历数据通过tushare获得。
        
        Return
        -------
            list,元素为交易日日期[u'2016-01-04',...,u'2016-06-17']
        '''
        data = ts.get_k_data('000001',self.start_date,
                             self.end_date,
                         index = True)
        data = data['date'].tolist()
        return data
    
    def _parepare_backtest_data(self):
        '''
        准备回测数据。
        '''
        pass
    

    
if __name__ == '__main__':
    a = GuosenSQLServer(events_queue = 1,
                        start_date = '20150101',end_date = '20160101')
    b = a.get_daily_data('600340','20160101','20170101')  
 

