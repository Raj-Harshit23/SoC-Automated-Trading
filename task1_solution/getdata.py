import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def data_extract(ticker_sym,price_type) :
    data = yf.download(ticker_sym, start='2023-05-01', end='2024-06-01')
    prices = data[price_type]

    prices.dropna(how='any',inplace=True)         #Data cleaning

    # Drop duplicate rows
    prices = prices.drop_duplicates()
    
    #Creating a datetime object
    prices.index=pd.to_datetime(prices.index)

    return prices

if __name__ == "__main__":
    data=data_extract('JSWENERGY.NS','Close')
    print(data)
