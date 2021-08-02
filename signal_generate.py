# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 13:16:14 2021

@author: Amit Chaudhary
"""

import pandas as pd
import numpy as np

# send list of market data objects to assign 
class SignalGen:
    
    def __init__(self, start_date, end_date , frequency, name , *args):
        self.start_date = start_date 
        self.end_date = end_date 
        self.frequency = frequency 
        self.name = name 
        date_series = pd.date_range(start=start_date,end=end_date, freq = frequency)
        signal_data = pd.DataFrame({'date':date_series})
        signal_data['date'] = signal_data['date'].dt.date
        signal_data['date_c'] = signal_data['date']
        signal_data.set_index('date',inplace=True)
        signal_data["signal"] = np.nan
        self.signal_data = signal_data
    
    def SetSignal(self,*args):
        if args is not None:
            if len(args) == 2: 
                fut = args[0]
                spot = args[1]
                for x in self.signal_data['date_c']:
                    #print(x)
                    fut_event = fut.getEventData(x)
                    spot_event = spot.getEventData(x)
                    self.expiry = fut.expiry
                    if fut_event is not None and spot_event is not None : 
                        spot_return = np.log(fut_event['price_close']) - np.log(spot_event['price_close'])
                        self.signal_data.loc[x,'signal'] = spot_return
    
    def SetSignalCom(self,*args):
        if args is not None:
            if len(args) > 2: 
                fut = args[0]
                spot = args[1]
                i_usdt = args[2]
                i_eth = args[3]
                for x in self.signal_data['date_c']:
                    #print(x)
                    fut_event = fut.getEventData(x)
                    spot_event = spot.getEventData(x)
                    i_usdt_event = i_usdt.getEventData(x)
                    i_eth_event = i_eth.getEventData(x)
                    self.expiry = fut.expiry
                    days_since = (self.expiry - x).days  
                    if fut_event is not None and spot_event is not None and i_usdt_event is not None and i_eth_event is not None  : 
                        #spot_return = np.log(fut_event['price_close']) - np.log(spot_event['price_close'])
                        spot_return = (fut_event['price_close'] - spot_event['price_close'])/spot_event['price_close']
                        self.signal_data.loc[x,'st_'+self.name] = spot_event['price_close']
                        self.signal_data.loc[x,'i_'+self.name] = (i_usdt_event['supply_rate']- i_eth_event['supply_rate'])
                        if days_since != 0:
                            spot_return = spot_return*(365/days_since) - (i_usdt_event['supply_rate']- i_eth_event['supply_rate'])
                            self.signal_data.loc[x,'fdis_'+self.name] = ((fut_event['price_close'] - spot_event['price_close'])/spot_event['price_close'])*(365/days_since)
                    
                        self.signal_data.loc[x,'signal'] = spot_return
                    
                    #print(x,fut_event['price_close'], spot_event['price_close'], days_since)
                    
                    
    def GetSignalEvent(self,event_date):
        if event_date in self.signal_data.index:
            m = self.signal_data.loc[event_date]
        else:
            m = None
        return m 
        
                