# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:14:46 2021

@author: Amit Chaudhary
"""

import pandas as pd
import numpy as np
import datetime as datetime

class ReturnsCalculation: 
    
    def __init__(self, order_feed, return_date, *args ):
        self.return_date = return_date 
        #self.start_date = order_feed.strategy.start_date 
        #self.end_date = order_feed.strategy.end_date 
        self.instruments = order_feed.instruments 
        self.ReturnAtDate = order_feed.OrdersExecuted
        ins_price_now = []
        ins_profit_yearly = []
        for ins in self.instruments:
            ins_price_now.append(ins+"_price_now")
            ins_profit_yearly.append(ins+"_profit_yearly")
        self.ins_price_now = ins_price_now 
        self.ins_profit_yearly  = ins_profit_yearly 
        
        for x in self.ins_price_now: 
            self.ReturnAtDate[x]=np.nan
        for x in self.ins_profit_yearly:
            self.ReturnAtDate[x]=np.nan
        self.ReturnAtDate = self.ReturnAtDate[self.ReturnAtDate['date_c'] < self.return_date]
            
    
    def FuturesExpiry(self,market_feed_ins,return_date):
        # should I adjust the price now and day
        a = (market_feed_ins.expiry- datetime.timedelta(days=7))
        if return_date > a:
            #print("adjusted date ", a)
            new_date = a
            return new_date
        else:
            #print("no adg", return_date)
            return return_date
    
    def CalculateReturn(self,order_feed):
        for x in self.ReturnAtDate['date_c']:
            sum_profit = 0
            sum_price = 0 
            for instrument in self.instruments:
                # get the market data at the return cal date
                price_feed_name = self.ins_price_now[self.instruments.index(instrument)]
                profit_feed_name = self.ins_profit_yearly[self.instruments.index(instrument)]
                market_feed= order_feed.getMarketFeed(instrument)
                return_date_adj = self.FuturesExpiry(market_feed,self.return_date)
                event_history = market_feed.getEventData(return_date_adj)
                market_feed_spot  =   order_feed.getMarketFeed("SPOT_ETH_USDT")
                event_spot =   market_feed_spot.getEventData(return_date_adj)
                past_spot =  market_feed_spot.getEventData(x)
                #print(return_date_adj, event_history["price_close"] )
                if event_history is not None: 
                   self.ReturnAtDate.loc[x,price_feed_name] = event_history["price_close"]
                   self.ReturnAtDate.loc[x,instrument+"_Stplus1"] = event_spot["price_close"]
                   self.ReturnAtDate.loc[x,instrument+"_St1"] = past_spot["price_close"]
                   orig_price =  self.ReturnAtDate.loc[x,instrument+"_price"]
                   now_price =   self.ReturnAtDate.loc[x,price_feed_name]
                   days_since = (return_date_adj - x).days 
                   profit =  self.ReturnAtDate.loc[x,instrument]*(now_price - orig_price)
                   
                   if days_since > 0 :
                       profit = profit
                   self.ReturnAtDate.loc[x,profit_feed_name] = profit
                
                if np.isnan(self.ReturnAtDate.loc[x,profit_feed_name]): 
                    profit = 0 
                else:
                    profit = self.ReturnAtDate.loc[x,profit_feed_name]
                sum_profit = sum_profit + profit
                if np.isnan(orig_price):
                    orig_price = 0 
                sum_price = sum_price + orig_price
                self.ReturnAtDate.loc[x,instrument+"_days"] = days_since
                
            self.ReturnAtDate.loc[x,"sum_profit"] = sum_profit
            self.ReturnAtDate.loc[x,"sum_price"] = sum_price
            
                   
    def CumulativeReturn(self,start_date):
        subset = self.ReturnAtDate[self.ReturnAtDate['date_c'] < self.return_date]
        pr = subset.fillna(0)['sum_profit'].sum()
        p = subset.fillna(0)['sum_price'].sum()
        cumulative_return = pr/p *(365/(self.return_date-start_date).days)
        return cumulative_return 
        
        
                