import pandas as pd
import numpy as np
import datetime
from getdata import fetch_extended_data

def RSI(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period]        #initial period
    # print(deltas.size)
    # print(prices.size)
    # print(seed.size)
    up = seed[seed >= 0].sum()
    down = -seed[seed < 0].sum()
    rs = up / down
    rsi = pd.Series(np.zeros_like(prices.values), index=prices.index)             #Initializing with zeroes
    rsi[:period+1] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)-1):
        delta = deltas[i]
        if delta >= 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        if(deltas[i-14]<0):
            down=down+deltas[i-14]
        else:
            up=up-deltas[i-14]

        if(deltas[i]<0):
            down=down-deltas[i]
        else:
            up=up+deltas[i]
        
        rs = up / down
        rsi.iloc[i+1] = 100. - 100. / (1. + rs)
    
    return rsi

if __name__ == "__main__":
    ##Set the data parameters
    ticker='JSWENERGY.NS'
    type='Close'
    period=14;
    data=fetch_extended_data(ticker,type,period)
    print(RSI(data))
