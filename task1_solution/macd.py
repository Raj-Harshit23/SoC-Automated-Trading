import pandas as pd
import numpy as np
import datetime
from getdata import data_extract
from sma import calculate_SMAs

def EMA(prices,period):
    initial_sma=calculate_SMAs(prices[:period],period)[0]