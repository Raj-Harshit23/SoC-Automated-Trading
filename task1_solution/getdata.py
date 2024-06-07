import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

def data_extract(ticker_sym,price_type,start='2024-05-01', end='2024-06-01') :
    data = yf.download(ticker_sym, start, end)
    prices = data[price_type]

    prices.dropna(how='any',inplace=True)         #Data cleaning

    # Drop duplicate rows
    prices = prices.drop_duplicates()
    
    #Creating a datetime object
    prices.index=pd.to_datetime(prices.index)

    return prices

def fetch_extended_data(ticket_sym,price_type,period,start_date='2024-05-01',end_date='2024-06-01') :
    date_str = start_date
    date_format = '%Y-%m-%d'
    date = dt.datetime.strptime(date_str, date_format)
    new_start=date-dt.timedelta(days=period*3)
    return data_extract(ticket_sym,price_type,new_start,end_date)
    

if __name__ == "__main__":
    data=data_extract('JSWENERGY.NS','Close')
    print(data)
