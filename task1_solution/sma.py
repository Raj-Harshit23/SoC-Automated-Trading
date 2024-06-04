import pandas as pd
import numpy as np
from getdata import data_extract

def calculate_SMAs(prices, short_window=20, long_window=50):
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()

    #Data cleaning
    short_ma.dropna(how='any',inplace=True)
    long_ma.dropna(how='any',inplace=True)

    return short_ma, long_ma

if __name__ == "__main__":
    ##Set the data parameters
    ticker='JSWENERGY.NS'
    type='Close'
    data=data_extract(ticker,type)
    print(calculate_SMAs(data))



