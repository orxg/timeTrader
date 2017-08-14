# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:25:31 2017

@author: LDH

定义事件。此模块暂时没用了。
"""

# event.py

from __future__ import print_function

from enum import Enum
from constants import *

__all__ = ['Event','BarEvent','OrderEvent',
           'SignalEvent','FillEvent']

EventType = Enum("EventType", "BAR SIGNAL ORDER FILL")


class Event(object):
    """
    Event是事件基础类。
    """
    @property
    def typename(self):
        return self.type.name

class BarEvent(Event):
    """
    Bar事件。
    """
    def __init__(
        self, ticker, datetime,
        open_price,high_price,low_price,close_price,
        volume,adj_close_price=None
    ):
        """
        初始化BarEvent。

        Parameters:
        ------------
        
            ticker 
                股票代码，如600340  
            datetime 
                bar的时间.支持datetime对象与'YYMMDD'格式 
            open_price
                bar的开盘
            high_price
                bar的最高
            low_price
                bar的最低
            close_price
                bar的收盘
            volume
                成交量
            adj_close_price
                前复权收盘

        """
        self.type = EventType.BAR
        self.ticker = ticker
        self.datetime = datetime
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.adj_close_price = adj_close_price

    def __str__(self):
        format_str = "Type: %s, Ticker: %s, Datetime: %s, " \
            "Open: %s, High: %s, Low: %s, Close: %s, " \
            "Adj Close: %s, Volume: %s" % (
                str(self.type), str(self.ticker), str(self.datetime),
                str(self.open_price),str(self.high_price), 
                str(self.low_price),str(self.close_price), 
                str(self.adj_close_price),
                str(self.volume)
            )
        return format_str

    def __repr__(self):
        return str(self)


class SignalEvent(Event):
    """
    策略产生的信号事件。
    """
    def __init__(self, ticker,action,quantity=None):
        """
        初始化信号事件。

        Parameters:
        ------------
            ticker
                股票代码。
            action 
                买卖动作,BUY或者SELL.
            quantity
                买卖数量。
        """
        self.type = EventType.SIGNAL
        self.ticker = ticker
        self.action = action
        self.quantity = quantity


class OrderEvent(Event):
    """
    下单事件。
    """
    def __init__(self, ticker, action, quantity):
        """
        初始化下单事件。

        Parameters
        ----------
            ticker
                股票代码
            action 
                买卖动作,BUY或者SELL
            quantity
                买卖数量
        """
        self.type = EventType.ORDER
        self.ticker = ticker
        self.action = action
        self.quantity = quantity

    def print_order(self):
        """
        输出事件信息。
        """
        print(
            "Order: Ticker=%s, Action=%s, Quantity=%s" % (
                self.ticker, self.action, self.quantity
            )
        )


class FillEvent(Event):
    """
    订单反馈事件。
    """

    def __init__(
        self, datetime, ticker,
        action, quantity,
        match_price,
        commission
    ):
        """
        初始化订单反馈事件。
        
        Parameters
        -----------
            datetime
                订单完成时间
            ticker 
                股票代码
            action 
                买卖方向
            quantity 
                成交数量
            match_price 
                成交价
            commission
                交易费用
        """
        self.type = EventType.FILL
        self.datetime = datetime
        self.ticker = ticker
        self.action = action
        self.quantity = quantity
        self.match_price = match_price
        self.commission = commission




if __name__ == '__main__':
    barEvent = BarEvent('600340','20160104',20,21,19.8,20.5,230000,20.5)
    signalEvent = SignalEvent('600340',BUY,34000)
    orderEvent = OrderEvent('600340',BUY,34000)
    fillEvent = FillEvent('20160104','600340',BUY,34000,20.7,50)
