# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 10:26:49 2021

@author: MarcelloCavalcanti
"""

import os
#import datetime as dt
import pandas as pd

os.chdir('C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/')
from account_manager import FlexNowExecution

file1 = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/Day_Orders.csv'
Order_Book = pd.read_csv(file1)
file2 = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/contract_specs.csv'
Order_Map = pd.read_csv(file2,index_col=0)
Order_Map['Expiry'] = pd.to_datetime(Order_Map['Expiry']).dt.strftime('%Y-%m-%d')
#Order_Map['Expiry'] = pd.to_datetime(Order_Map['Expiry'])



def execute(symbol:str, mic_code:str, side:str, quantity:int, maturity_date: str):
    FlexNowExecution(session_type='uat').execute_order(symbol=symbol, asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code=mic_code, side=side,
                                                       quantity=quantity,order_type='Market',maturity_date=maturity_date,
                                                       broker='SOCGENsim', strategy_note='MC_test')
    print('Trade to %s %i %s at Market sent to FlexNow' % (side,quantity,symbol))
    


if __name__ == '__main__':

    for i in range(len(Order_Book)):
        
        execute(symbol = Order_Book.loc[Order_Book.index[i],'Ticker'], mic_code = Order_Map.loc[Order_Book.loc[Order_Book.index[i],'Ticker'][0:2],'Mic_Code'],
                side = Order_Book.loc[Order_Book.index[i],'Trade'], quantity = int(Order_Book.loc[Order_Book.index[i],'Quantity']) ,
                maturity_date = Order_Map.loc[Order_Book.loc[Order_Book.index[i],'Ticker'][0:2],'Expiry'])













'''
Order_Book.loc[Order_Book.index[1],'Trade']
Order_Book.loc[Order_Book.index[1],'Ticker'][0:2]
type(Order_Map.loc[Order_Book.loc[Order_Book.index[1],'Ticker'][0:2],'Expiry'])
type('2021-12-17')

if __name__ == '__main__':
    FlexNowExecution(session_type='uat').execute_order(symbol='ESU1 Index', asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code='XCME', side='BUY',
                                                       quantity=100,order_type='Market',maturity_date='2021-12-17',
                                                       broker='SOCGENsim', strategy_note='MC_test')
    
    
    
    FlexNowExecution(session_type='uat').execute_order(symbol='ABC', asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code='XNYS', side='SELL',
                                                       quantity=100, booking_type= 'Swap',
                                                       broker='SOCGENsim', strategy_note='MC_test')
    
    FlexNowExecution(session_type='uat').execute_order(symbol='ABC', asset_class='Equity', currency='USD',
                                                       region='NorthAmerica', country='US', mic_code='XNYS', side='BUY',
                                                       quantity=100,
                                                       broker='SOCGENsim', strategy_note='MC_test')


'''


