# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 14:58:16 2021

@author: Amit Chaudhary
"""

import pandas as pd
import numpy as np

class Strategy: 
    
    def __init__(self,start_date, end_date , frequency, names, *args):
        self.start_date = start_date 
        self.end_date = end_date 
        self.frequency = frequency 
        self.instruments = names
        date_series = pd.date_range(start=start_date,end=end_date, freq = frequency)
        strategy_data = pd.DataFrame({'date':date_series})
        strategy_data['date'] = strategy_data['date'].dt.date
        strategy_data['date_c'] = strategy_data['date']
        strategy_data.set_index('date',inplace=True)
        for arg in args:
            strategy_data[arg] = np.nan
        self.strategy_data = strategy_data
    
    def SetStrategy(self,*args):
        if len(args) > 0  :
            for instrument in self.instruments:
                # get the signal object of the instrument 
                print("searching for ", instrument )
                for arg in args: 
                    if arg.name == instrument:
                        print("here")
                        signal_first = arg
                for x in self.strategy_data['date_c']:
                    signal_event = signal_first.GetSignalEvent(x)
                    if signal_event['signal'] <= -0.05:
                        strategy=-1
                    elif signal_event['signal'] > 0:
                        strategy=1
                    else:
                        strategy = 0 
                    
                    # close to expiry 
                    if (signal_first.expiry - x).days <= 7 : 
                        strategy = 0 
                    
                    self.strategy_data.loc[x,instrument] = strategy
            
                
        