# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 16:26:48 2021

@author: Amit Chaudhary
"""
import numpy as np

class MarketData:
    def __init__(self,feed,name,*args):
        self.feed = feed
        self.name = name
        if len(args) > 0 :
            self.expiry = args[0]
        else:
            self.expiry = np.nan
    
    def getEventData(self,event_date):
        if event_date in self.feed.index:
            m = self.feed.loc[event_date]
        else:
            m = None
        return m 