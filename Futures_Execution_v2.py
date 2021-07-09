# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:26:49 2021

@author: MarcelloCavalcanti
"""

import os#, re
#import datetime as dt
import pandas as pd
import numpy as np

os.chdir('C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/')
from account_manager import FlexNowExecution

file1 = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/Day_Orders.csv'
Order_Book = pd.read_csv(file1)
file2 = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/contract_specs.csv'
Order_Map = pd.read_csv(file2,index_col=0)
Order_Map['Expiry'] = pd.to_datetime(Order_Map['Expiry']).dt.strftime('%Y-%m-%d')
#Order_Map['Expiry'] = pd.to_datetime(Order_Map['Expiry'])

    
if __name__ == '__main__':

    for i in range(len(Order_Book)):
        
        FlexNowExecution(session_type='uat').execute_order(symbol = Order_Book.loc[Order_Book.index[i],'Ticker'], asset_class = 'Equity', currency = 'USD',
                        region = 'NorthAmerica', country = 'US', mic_code = Order_Map.loc[Order_Book.loc[Order_Book.index[i],'Ticker'][0:2],'Mic_Code'],
                        side = Order_Book.loc[Order_Book.index[i],'Trade'], quantity = int(Order_Book.loc[Order_Book.index[i],'Quantity']),
                        order_type = Order_Book.loc[Order_Book.index[i],'Type'], maturity_date = Order_Map.loc[Order_Book.loc[Order_Book.index[i],'Ticker'][0:2],'Expiry'],
                        limit_price = np.where(Order_Book.loc[Order_Book.index[i],'Type'] == 'Limit', Order_Book.loc[Order_Book.index[i],'Price'], None).item(),
                        stop_price = np.where(Order_Book.loc[Order_Book.index[i],'Type'] == 'Stop', Order_Book.loc[Order_Book.index[i],'Price'], None).item(),
                        broker='SOCGENsim', strategy_note='MC_test')
        
        print('Trade to %s %i %s type %s sent to FlexNow' % (Order_Book.loc[Order_Book.index[i],'Trade'],int(Order_Book.loc[Order_Book.index[i],'Quantity']),Order_Book.loc[Order_Book.index[i],'Ticker'],Order_Book.loc[Order_Book.index[i],'Type']))




