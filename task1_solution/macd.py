import pandas as pd
import numpy as np
import datetime
from getdata import fetch_extended_data
from sma import calculate_SMAs

def EMA(prices,period):
    initial_sma=calculate_SMAs(prices,period)[0]
    print(initial_sma.size)     
    ema=pd.Series(np.zeros_like(prices),index=prices.index) #initialising

    ema.iloc[:period]=initial_sma[:period]
    multiplier=2/(period+1)
    for t in range(period+1,len(prices)):
        ema.iloc[t]=prices.iloc[t]*multiplier+ema.iloc[t-1]*(1-multiplier)

    return ema


if __name__ == "__main__":
    ##Set the data parameters
    ticker='JSWENERGY.NS'
    type='Close'
    period=14;
    data=fetch_extended_data(ticker,type,period)
    print(EMA(data,12))
