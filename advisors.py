import ccxt
import config
import schedule
import pandas as pd
from talib import MA_Type
import pprint
import talib as ta

pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')

import numpy as np
from datetime import datetime
import time

exchange = ccxt.binance({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=100)
df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  

df['RSI'] = ta.RSI(df['close'])

def dataAcquire():
    bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms') 
    return df

def RsiAdvisor(data, Upper=70, Lower=30):
    data['RSI'] = ta.RSI(data['close'])
    RsiIndex = data.iloc[-1]['RSI']
    print("The RSI index now is {}".format(RsiIndex))
    if RsiIndex > Upper:
        print("RSI strategy suggest you to sell!")
    elif RsiIndex < Lower:
        print("RSI strategy suggest you to buy!")
    else:
        print("RSI strategy suggest you to hold!")

def BBandAdvisor(data,period = 6):
    close = data['close'].to_numpy()
    upper, middle, lower = ta.BBANDS(close, matype= MA_Type.T3)
    MA_close = ta.SMA(close,period)
    th = 0.05
    if MA_close[-2] < upper[-2] and MA_close[-2] > middle[-2]:
        if close[-1] > upper[-1]*(1+th):
            print("BBand strategy suggest you to sell! 0.05 % Higher than upper boundary")
        elif close[-1] < middle[-1]*(1+th):
            print("BBand strategy suggest you to buy! 0.05 % lower than middle boundary")
        else:
            print("BBand strategy suggest you to hold!")
    
    elif MA_close[-2]< middle[-2] and MA_close[-2]> lower[-2]:
        if close[-1] > middle[-1]*(1-th):
            print("BBand strategy suggest you to sell! 0.05 % Higher than middle boundary")
        elif close[-1] < lower[-1]*(1-th):
            print("BBand strategy suggest you to buy! 0.05 % Higher than lower boundary")
        else:
            print("BBand strategy suggest you to hold!")

    else:
        print("BBand strategy suggest you to hold!")

def MACDAdvisor(data,fastperiod = 12, slowperiod = 26, signalperiod = 9):
    close = data['close'].to_numpy()
    macd, macdsignal, macdhist = ta.MACD(close, 12, 26, 9)
    MA_macdist = ta.SMA(macdhist,2)
    if macdhist[-2]*macdhist[-1] < 0:
        if macd[-2] < macdsignal[-2]:
            print("MACD strategy suggest you to buy! Golden Cross occurred.")
        elif macd[-2] > macdsignal[-2]:
            print("MACD strategy suggest you to sell! Death Cross occurred.")
    else:
        if macdhist[-1] > MA_macdist[-2]:
            print("MACD strategy suggest you to buy! Turning point occurred.")
        elif macdhist[-1] < MA_macdist[-2]:
            print("MACD strategy suggest you to sell! Turning point occurred.")
        else:
            print("MACD strategy suggest you to hold!")

# def SupperTrend(data):

def BarUpDn(data):
        # if open[i] > close[i-1], close[i-1] > open[i-1] enter long
        # if open[i] < close[i-1], close[i-1] < open[i-1] enter short
    close = data['close'].to_numpy()
    open = data['open'].to_numpy()
    if open[-1] > close[-2] and close[-2] > open[-2]:
        print("BarUpDn strategy suggest you to buy!")
    elif open[-1] < close[-2] and close[-2] < open[-2]:
        print("BarUpDn strategy suggest you to sell!")
    else:
        print("BarUpDn strategy suggest you to hold!")

def OutSideBar(data):
        #if low[i] < low[i-1], high[i] > high[i-1] : outside bar strategy
        # red bar sell, green bar buy
    close = data['close'].to_numpy()
    high = data['high'].to_numpy()
    low = data['low'].to_numpy()
    open = data['open'].to_numpy()
    if low[-1] < low[-2] and high[-1] > high[-2]:
        if open[-1] < close[-1]:
            print("OutSideBar strategy suggest to you buy!")
        else:
            print("OutSideBar strategy suggest to you sell!")
    else:
        print("OutSideBar strategy suggest to you hold!")

def SlowFastSMA(data,fastPeriod = 7,slowPeriod = 14):
        # If not in position and FastSMA > SLOWSMA ->BUY
        # If in position and SlowSMA > FastSMA -> Sell
    close = data['close'].to_numpy()
    fastSma = ta.SMA(close,fastPeriod)
    slowSma = ta.SMA(close,slowPeriod)
    if (fastSma[-2]-slowSma[-2])*(fastSma[-1]-slowSma[-1]) < 0:
        if fastSma[-1] > slowSma[-1]:
            print("SlowFastSMA strategy suggest you to buy!")
        else:
            print("SlowFastSMA strategy suggest you to sell!")
    else:
        print("SlowFastSMA strategy suggest you to hold!")


def run_bot():
    df = dataAcquire()
    print("----------------------------------------------------------------")
    pprint.pprint(df.tail(3))
    RsiAdvisor(df)
    BBandAdvisor(df)
    MACDAdvisor(df)
    BarUpDn(df)
    OutSideBar(df)
    SlowFastSMA(df)
    # givingAdvise()


schedule.every(60).seconds.do(run_bot)


while True:
    schedule.run_pending()
    time.sleep(1)