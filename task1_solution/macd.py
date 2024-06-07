import pandas as pd
import numpy as np
import datetime
from getdata import fetch_extended_data
from sma import SMAs

def EMA(prices,period):
    initial_sma=SMAs(prices,period)[0]
    # print(initial_sma.size)     
    ema=pd.Series(np.zeros_like(prices),index=prices.index) #initialising

    ema.iloc[:period]=initial_sma[:period]
    multiplier=2/(period+1)
    for t in range(period,len(prices)):
        ema.iloc[t]=prices.iloc[t]*multiplier+ema.iloc[t-1]*(1-multiplier)

    return ema

def MACD(prices, fast=12, slow=26, signal=9):
    ema_fast=EMA(prices,fast)
    ema_slow=EMA(prices,slow)

    macd_line=ema_fast-ema_slow
    signal_line=EMA(macd_line,signal)

    hist=macd_line-signal_line

    return macd_line,signal_line,hist


if __name__ == "__main__":
    ##Set the data parameters
    ticker='JSWENERGY.NS'
    type='Close'
    period=12;
    data=fetch_extended_data(ticker,type,period)
    # print(EMA(data,12))
    print("-----")
    print(MACD(data))
    
