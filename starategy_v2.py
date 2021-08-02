# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 15:43:40 2021

@author: Amit Chaudhary
"""


"""

architecture 

1) data stream  + currency exchanges 
2) signal 
3) portfolio construction 
5) return 

basic class or not 

1) data stream 

series of daily prices 
1) Futures / forward contract / spot prices

    Identifier : Asset_ID  start_date end_date expiry_data  
    DATE  PRICE   VOLUME ..... 
    ....  .....    ....
    ....  .....    .....  

2) Signal 
    DATE asset1_SiGNAL asset_2Signal asset3_signal 
    
3) Portfolio construction 
        parameter : interval (eg weekly) 
        DATE ASSET1 holding1 price1 ASSET2 holding2 price2 ASSET3 .. 
        wk1
        wk2
        wk3
        wk4
        
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from market_data import MarketData
from signal_generate import SignalGen
from strategy import Strategy
from order_management import OrderManagement
from returns_calculate import ReturnsCalculation
import datetime

def getDateformat(input_string):
    date_str = input_string # The date - 29 Dec 2017
    format_str = '%Y-%m-%d' # The format
    event_time = datetime.datetime.strptime(date_str, format_str).date()
    return event_time
    
ETH_USD_200925 = pd.read_csv("ETH_USD_200925.csv")
ETH_USD_200925['date'] = pd.to_datetime(ETH_USD_200925['time_period_start']).dt.date
ETH_USD_200925['date_c'] = ETH_USD_200925['date']
ETH_USD_200925.set_index('date',inplace=True)
#future_eth_usd_200925 = data
expiry = getDateformat("2020-09-25")

ETH_USD_200925_ins = MarketData(ETH_USD_200925,"ETH_USD_200925",expiry)

ETH_USD_201225 = pd.read_csv("ETH_USD_201225.csv")
ETH_USD_201225['date'] = pd.to_datetime(ETH_USD_201225['time_period_start']).dt.date
ETH_USD_201225['date_c'] = ETH_USD_201225['date']
ETH_USD_201225.set_index('date',inplace=True)

expiry = getDateformat("2020-12-25")

ETH_USD_201225_ins = MarketData(ETH_USD_201225,"ETH_USD_201225",expiry)

ETH_USD_210326 = pd.read_csv("ETH_USD_210326.csv")
ETH_USD_210326['date'] = pd.to_datetime(ETH_USD_210326['time_period_start']).dt.date
ETH_USD_210326['date_c'] = ETH_USD_210326['date']
ETH_USD_210326.set_index('date',inplace=True)

expiry = getDateformat("2021-03-26")

ETH_USD_210326_ins = MarketData(ETH_USD_210326,"ETH_USD_210326",expiry)

ETH_USD_210625 = pd.read_csv("ETH_USD_210625.csv")
ETH_USD_210625['date'] = pd.to_datetime(ETH_USD_210625['time_period_start']).dt.date
ETH_USD_210625['date_c'] = ETH_USD_210625['date']
ETH_USD_210625.set_index('date',inplace=True)

expiry = getDateformat("2021-06-25")

ETH_USD_210625_ins = MarketData(ETH_USD_210625,"ETH_USD_210625",expiry)


SPOT_ETH_USDT = pd.read_csv("SPOT_ETH_USDT.csv")
SPOT_ETH_USDT['date'] = pd.to_datetime(SPOT_ETH_USDT['time_period_start']).dt.date
SPOT_ETH_USDT['date_c'] = SPOT_ETH_USDT['date']
SPOT_ETH_USDT.set_index('date',inplace=True)

SPOT_ETH_USDT_ins = MarketData(SPOT_ETH_USDT,"SPOT_ETH_USDT")


# include the compound data as market data object 

# COMP market date for USDT  
USDT_COMPOUND = pd.read_csv("Compound_USDT.csv")
USDT_COMPOUND['date'] = pd.to_datetime(USDT_COMPOUND['date']).dt.date
USDT_COMPOUND['date_c'] = USDT_COMPOUND['date']
USDT_COMPOUND.set_index('date',inplace=True)
USDT_COMPOUND_ins = MarketData(USDT_COMPOUND,"USDT_COMPOUND")

#COMP market data for ETH
ETH_COMPOUND = pd.read_csv("Compound_ETH.csv")
ETH_COMPOUND['date'] = pd.to_datetime(ETH_COMPOUND['date']).dt.date
ETH_COMPOUND['date_c'] = ETH_COMPOUND['date']
ETH_COMPOUND.set_index('date',inplace=True)
ETH_COMPOUND_ins = MarketData(ETH_COMPOUND,"USDT_COMPOUND")



#get signal 
signal_eth_200925 = SignalGen("2020-08-05","2021-06-24","D","ETH_USD_200925")
signal_eth_200925.SetSignalCom(ETH_USD_200925_ins,SPOT_ETH_USDT_ins,USDT_COMPOUND_ins, ETH_COMPOUND_ins)

signal_eth_201225 = SignalGen("2020-08-05","2021-06-24","D","ETH_USD_201225")
signal_eth_201225.SetSignalCom(ETH_USD_201225_ins,SPOT_ETH_USDT_ins,USDT_COMPOUND_ins, ETH_COMPOUND_ins)

signal_eth_210326 = SignalGen("2020-08-05","2021-06-24","D","ETH_USD_210326")
signal_eth_210326.SetSignalCom(ETH_USD_210326_ins,SPOT_ETH_USDT_ins, USDT_COMPOUND_ins, ETH_COMPOUND_ins )

signal_eth_210625 = SignalGen("2020-08-05","2021-06-24","D","ETH_USD_210625")
signal_eth_210625.SetSignalCom(ETH_USD_210625_ins,SPOT_ETH_USDT_ins, USDT_COMPOUND_ins, ETH_COMPOUND_ins )


a = signal_eth_200925.signal_data
b=  signal_eth_201225.signal_data

instruments = ["ETH_USD_200925", "ETH_USD_201225", "ETH_USD_210326","ETH_USD_210625"]
strategy_eth = Strategy("2020-08-05","2021-06-24","D",instruments )
strategy_eth.SetStrategy(signal_eth_200925,signal_eth_201225, signal_eth_210326,signal_eth_210625)

a = strategy_eth.strategy_data

order_ins = OrderManagement(strategy_eth, ETH_USD_200925_ins, ETH_USD_201225_ins, ETH_USD_210326_ins, ETH_USD_210625_ins,SPOT_ETH_USDT_ins)
order_ins.OrderExecuteAtClose()

date_returns  = getDateformat('2021-05-11')
return_ins = ReturnsCalculation(order_ins, date_returns)
return_ins.CalculateReturn(order_ins)

start  = getDateformat('2020-08-05')
temp = return_ins.CumulativeReturn(start)
ret = return_ins.ReturnAtDate

# export to csv 
ret.to_csv("strategy_data_v2.csv")

# loop for returns 
num_days = (date_returns - start).days
datelist = []
for x in range(1,num_days):
    datelist.append(start + datetime.timedelta(days=x))

return_dict= {}
for x in datelist:
    return_ins = ReturnsCalculation(order_ins, x)
    return_ins.CalculateReturn(order_ins)
    return_dict[x]=return_ins.CumulativeReturn(start)
    print(x, "return", return_dict[x])

dates = list(return_dict.keys())           
c_ret = list(return_dict.values())

c_ret_1 = c_ret  # r = 38.4%
c_ret_2 = c_ret

plt.xticks(rotation=45)
plt.plot(dates,c_ret_1,label = "Strategy 1: Annualized return - 55.4%. ")
plt.plot(dates,c_ret_2, label = "Strategy 2 Annualized retuns - 120.3%")
plt.title('Cumulative returns')
plt.ylabel('returns')
plt.xlabel('time')
plt.legend()
plt.savefig('returns.png')



#####################################


a = signal_eth_200925.signal_data.rename(columns={'signal': 'signal_a'})
b=  signal_eth_201225.signal_data.rename(columns={'signal': 'signal_b'})
c = signal_eth_210326.signal_data.rename(columns={'signal': 'signal_c'})
d=  signal_eth_210625.signal_data.rename(columns={'signal': 'signal_d'})
ret = return_ins.ReturnAtDate

merged = a.merge(b, on='date_c', how='left').merge(c, on='date_c', how='left').merge(d, on='date_c', how='left').merge(ret, on='date_c', how='left')

# subset the column 

a_new = merged[merged['ETH_USD_200925_days'] > 0]
a_new['forward_discount'] = a_new['fdis_ETH_USD_200925']
a_new['i_diff']= a_new['i_ETH_USD_200925']
a_new['price_change']=((a_new['ETH_USD_200925_Stplus1'] - a_new['ETH_USD_200925_St1'])/a_new['ETH_USD_200925_St1'])*(365/a_new['ETH_USD_200925_days'])
a_new['excess_ret']=  ((a_new['ETH_USD_200925_price_now']- a_new['ETH_USD_200925_price'])/a_new['ETH_USD_200925_price'] )*(365/a_new['ETH_USD_200925_days'])
a_new['risk_var'] = a_new['signal_a']


b_new = merged[merged['ETH_USD_201225_days'] > 0]
b_new['forward_discount'] = b_new['fdis_ETH_USD_201225']
b_new['i_diff']= b_new['i_ETH_USD_201225']
b_new['price_change']=((b_new['ETH_USD_201225_Stplus1'] - b_new['ETH_USD_201225_St1'])/b_new['ETH_USD_201225_St1'])*(365/b_new['ETH_USD_201225_days'])
b_new['excess_ret']=  ((b_new['ETH_USD_201225_price_now']- b_new['ETH_USD_201225_price'])/b_new['ETH_USD_201225_price'] )*(365/b_new['ETH_USD_201225_days'])
b_new['risk_var'] = b_new['signal_b']

c_new = merged[merged['ETH_USD_210326_days'] > 0]
c_new['forward_discount'] = c_new['fdis_ETH_USD_210326']
c_new['i_diff']= c_new['i_ETH_USD_210326']
c_new['price_change']=((c_new['ETH_USD_210326_Stplus1'] - c_new['ETH_USD_210326_St1'])/c_new['ETH_USD_210326_St1'])*(365/c_new['ETH_USD_210326_days'])
c_new['excess_ret']=  ((c_new['ETH_USD_210326_price_now']- c_new['ETH_USD_210326_price'])/c_new['ETH_USD_210326_price'] )*(365/c_new['ETH_USD_210326_days'])
c_new['risk_var'] = c_new['signal_c']

d_new = merged[merged['ETH_USD_210625_days'] > 0]
d_new['forward_discount'] = d_new['fdis_ETH_USD_210625']
d_new['i_diff']= d_new['i_ETH_USD_210625']
d_new['price_change']=((d_new['ETH_USD_210625_Stplus1'] - d_new['ETH_USD_210625_St1'])/d_new['ETH_USD_210625_St1'])*(365/d_new['ETH_USD_210625_days'])
d_new['excess_ret']=  ((d_new['ETH_USD_210625_price_now']- d_new['ETH_USD_210625_price'])/d_new['ETH_USD_210625_price'] )*(365/d_new['ETH_USD_210625_days'])
d_new['risk_var'] = d_new['signal_d']

dframes = [c_new,d_new]
append_data = pd.concat(dframes)

a_new.to_csv("a_new.csv")
b_new.to_csv("b_new.csv")
c_new.to_csv("c_new.csv")
d_new.to_csv("d_new.csv")

append_data.to_csv("append_new.csv")


#ordermangement system (buy at the some price) inventory style based on execution 
  # price feed / ask / bid and flag of execution at this price (another column)
# p&l statement based on daily return  




#generate time series for daily signals 
date_series = pd.date_range(start="2020-09-01",end="2021-06-24", freq =  "D")
market_data = pd.DataFrame({'date':date_series})
market_data['date'] = market_data['date'].dt.date
market_data['date_c'] = market_data['date']
market_data.set_index('date',inplace=True)


market_data = pd.merge(market_data,SPOT_ETH_USDT,how = "left", on=['date']) 
market_data = pd.merge(market_data,ETH_USD_200925,how = "left", on=['date']) 


position_time = "1W"  # simple portfolio holding time 

column_names = ["ETH_USD_200925_sig"]
signal_frame = pd.DataFrame(index=market_data.index, columns = column_names)


def signal_logic(event_date, market_input, signal_input):
    m = market_input.loc[event_date]
    # signal logic 
    spot_return = np.log(m['price_close_y']) - np.log(m['price_close_x'])
    if spot_return > 0:
        signal = 1 
    elif spot_return < 0:
        signal= -1 
    else:
        signal = 0 
    print(signal)
    signal_input.loc[event_date,'ETH_USD_200925_sig'] = signal
    
    print(signal_input.loc[event_date,:])
    
    logic = 1 
    
    return logic

def signal_construction(market_data, signal_frame):
    for x in market_data['date_c']:
        logic = signal_logic(x,market_data,signal_frame)
        sig_row  = signal_frame.loc[x]
        break
        #print(sig_row)
    
    return logic   

signal_construction(market_data, signal_frame)
