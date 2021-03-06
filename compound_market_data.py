# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 10:55:20 2021

@author: Amit Chaudhary
"""


import requests
import pandas as pd
from itertools import tee
from typing import Iterable, Tuple, TypeVar, List


import datetime as dt

T = TypeVar('T')


token_addresses = { 'cdai': '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',
                    'ceth': '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
                    'crep': '0x158079ee67fce2f58472a96584a73c7ab9ac95c1',
                    'csai': '0xf5dce57282a584d2746faf1593d3121fcac444dc',
                    'cusdc': '0x39aa39c021dfbae8fac545936693ac917d5e7563',
                    'cwbtc': '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4',
                    'czrx': '0xb3319f5d18bc0d84dd1b4825dcde5d5f7266d407'}

variables = ['total_borrows_history', 'total_supply_history', 'utilization_ratio', 'spread', 'borrow_rates', 'supply_rates', 'exchange_rates']

url = 'https://api.compound.finance/api/v2/market_history/graph'

end_date = int(dt.datetime(2021, 8, 1, 0).timestamp())
start_date = int((dt.datetime(2021, 8, 1, 0) - dt.timedelta(days = 580)).timestamp())

# start_date = int((dt.datetime(2020, 7, 5, 0) - dt.timedelta(days = 1000)).timestamp())


def generate_dates(start: dt.datetime, end: dt.datetime,
                   buckets_count: int) -> Iterable[dt.datetime]:
    """Generates a list of ``buckets_count + 1`` dates between
    ``start`` and ``end``
    :param start: the first date of the sequence to generate
    :param end: the last date of the sequence to generate
    :param buckets_count: the number of dates to generate - 1
    """
    diff = (end - start) / buckets_count
    for i in range(buckets_count):
        yield start + diff * i
    yield end


def pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """Returns an iterable of shifted pairs
    >>> list(pairwise(['a', 'b', 'c', 'd']))
    [('a', 'b'), ('b', 'c'), ('c', 'd')]
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

list_dates = list(pairwise(generate_dates(start=start_date, 
                    end=end_date, buckets_count=580)))

#def format_date(x, pos=None):
#     return dates.num2date(x).strftime('%Y-%m-%d')

def make_dataframe(token: str, days):
    '''
    Build money-market dataframes. 
    '''
    master_df = pd.DataFrame()

    for day in days:

        params = {'asset': token_addresses[token],
                'min_block_timestamp': int(day[0]),
                'max_block_timestamp': int(day[1]),
                'num_buckets': 1}

        response = requests.get(url = url, params=params)
        status_code = int(response.status_code)
        
        #return response
        response = response.json()
        #print(params)
        st = dt.datetime.utcfromtimestamp(day[0]).strftime('%Y-%m-%d %H:%M:%S')
        en = dt.datetime.utcfromtimestamp(day[1]).strftime('%Y-%m-%d %H:%M:%S')
        print("extract data from ", st, "to", en)
        if status_code==200:
            print("Success")
        else:
            print("failure", " code = ", status_code )
        if status_code==500:
            #print("error in the data from ", day[0], "to", day[1])
            continue
        
        if response['borrow_rates'] == []:
            #print("error in the data from ", day[0], "to", day[1])
            continue

        rate_variables = ['borrow_rates', 'exchange_rates', 'supply_rates']

        df = pd.DataFrame()

        for key in rate_variables:
            df_temp = pd.DataFrame(response[key])
            df_temp['date'] = pd.to_datetime(df_temp['block_timestamp'], unit='s')
            df_temp.set_index('date', inplace = True)
            df_temp = df_temp[['rate']]
            df_temp = df_temp.rename(columns={'rate': str(key)})
            df = pd.concat([df, df_temp], axis=1)

        stock_variables = ['total_borrows_history', 'total_supply_history']

        for key in stock_variables:
            df_temp = pd.DataFrame(response[key])
            df_temp['date'] = pd.to_datetime(df_temp['block_timestamp'], unit='s')
            df_temp.set_index('date', inplace = True)
            df_temp = df_temp[['total']]
            df_temp = pd.concat([df_temp.drop(['total'], axis=1), df_temp['total'].apply(pd.Series)], axis=1)
            df_temp = df_temp.rename(columns={'value': str(key)})
            df = pd.concat([df, df_temp], axis=1)

        df['total_borrows_history'] = pd.to_numeric(df['total_borrows_history'], downcast="float")
        df['total_supply_history'] = pd.to_numeric(df['total_supply_history'], downcast="float")
        df['total_supply_history'] = df['total_supply_history'] * df['exchange_rates']

        df['utilization_ratio'] = df['total_borrows_history'] / df['total_supply_history']
        df['spread'] = df['borrow_rates']- df['supply_rates']

        master_df = master_df.append(df)
    
    return master_df


BaseDir = "C:\\Users\\Amit Chaudhary\\Warwick\Mr-Robot\compound_market_data\\"

for token in token_addresses:
    print(token)
    data_fetch = make_dataframe(token=token, days=list_dates)
    data_fetch_new = data_fetch.rename(columns={'date':'date_time',
                                            'borrow_rates':'borrow_rate', 
                                            'supply_rates':'supply_rate',
                                            'total_borrows_history':'total_borrows',
                                            'total_supply_history':'total_supply',
                                            'utilization_ratio':'utilization_rate'})
            
    data_fetch_new = data_fetch_new.drop(columns=['exchange_rates','spread'])
    print("Saving data for  ", token)
    data_fetch_new.to_csv(BaseDir+ token+ ".csv")
    break


    