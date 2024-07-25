ticker=input("Enter the ticker symbol: ")
print("Whats gonna happen the next trading day? Lemme think for a while...")

import yfinance as yf
import pandas as pd
import os
import pandas_ta as ta
import numpy as np
from sklearn.preprocessing import StandardScaler

def data(ticker):
  df = yf.Ticker(ticker)
  df = df.history(period="max")
  df.index = pd.to_datetime(df.index)
  del df["Dividends"]
  del df["Stock Splits"]
  df = df.loc["2014-01-01":].copy()
  df["Target"] = (df["Close"] > df["Open"]).astype(int).shift(-1)   ##Binary target...tomorrow increase or decrease direction as an output to be decided by todays statistics
  # frequency = df['Target'].value_counts()
  # print(frequency)
  df.dropna(inplace=True)
  return df

# Calculating technical indicators using pandas_ta
def add_features(df):
    df['EMA_2'] = ta.ema(df['Close'], length=2)
    df['EMA_5'] = ta.ema(df['Close'], length=5)
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    df['EMA_100'] = ta.ema(df['Close'], length=100)

    df['RSI_14'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    df['OBV'] = ta.obv(df['Close'], df['Volume'])

    # Lagged features (kind of last few rows to predict the next row)
    for lag in range(1, 10):  
    # lag-=1
        df[f'Close_t-{lag}'] = df['Close'].shift(lag)
        df[f'Open_t-{lag}'] = df['Open'].shift(lag)
        df[f'High_t-{lag}'] = df['High'].shift(lag)
        df[f'Low_t-{lag}'] = df['Low'].shift(lag)
        df[f'Volume_t-{lag}'] = df['Volume'].shift(lag)

    df = df.dropna()
    return df

df=data(ticker)
df_added=add_features(df)

# Define lagged features and technical indicators
lagged_features = [f'Close_t-{i}' for i in range(1, 10)] + [f'Open_t-{i}' for i in range(1, 10)] + [f'Volume_t-{i}' for i in range(1, 10)]
featuresq = ['EMA_2', 'EMA_5','EMA_20','EMA_100', 'RSI_14', 'MACD_signal', 'ATR', 'OBV', 'Close', 'Volume']

# Combine all features
all_features = featuresq + lagged_features
# Feature normalization
scaler = StandardScaler()
df[all_features] = scaler.fit_transform(df[all_features])

# Preparing the features and target
X = df_added[all_features]
y = df_added['Target']  

#Training the model
from sklearn.ensemble import RandomForestClassifier
model3=RandomForestClassifier(n_estimators=500, min_samples_split=19, random_state=6,min_samples_leaf=1, max_features=25,n_jobs=-1)

#Data is the last 350 days prior to today
X_train=X[-351:-1]
y_train=y[-351:-1]

model3.fit(X_train,y_train)

prediction=model3.predict(X.iloc[-1:]) #Thats the latest info to make prediction for tomorrow
threshold=0.5           #Can customise
if(prediction>threshold) :
   print("I think INCREASE.")
else:
   print("DECREASE.(maybe :) ) ")


