# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:11:33 2021

@author: Amit Chaudhary
"""

import pandas as pd
import numpy as np

class OrderManagement: 
    
    def __init__(self, strategy, *args ):
        self.instruments = strategy.instruments
        self.OrdersExecuted = strategy.strategy_data
        self.MarketData = args
        ins_price = []
        for ins in self.instruments:
            ins_price.append(ins+"_price")
        self.ins_price = ins_price 
        for x in self.ins_price: 
            self.OrdersExecuted[x]=np.nan
        
    def getMarketFeed(self,inst):
        for i in self.MarketData:
            if i.name == inst:
                return i
    
    def OrderExecuteAtClose(self):
        # execute the orders 
        for instrument in self.instruments: 
            market_feed= self.getMarketFeed(instrument)
            price_feed_name = self.ins_price[self.instruments.index(instrument)]
            for x in self.OrdersExecuted['date_c']:
                #print("date:",x)
                event_history = market_feed.getEventData(x)
                if event_history is not None: 
                   self.OrdersExecuted.loc[x,price_feed_name] = event_history["price_close"]
               
            
                