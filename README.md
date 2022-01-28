# Crypto Strategy Advisor
A real time suggestion from different crypto trading strategies

# Excuation Steps:
Step 1. Type your binance secret key and binance api key in config.py.

Step 2. Run the advisor.py for acquire real time suggestion of different crypto trading strategies.

# Explaination of Strategies:

# RsiAdvisor: 
if RSI > 70 Sell the crypto
if RSI < 30 Buy the crypto

# BBandAdvisor: Bolling Band Trading Strategy.

# MACDAdvisor: Golden Cross Buy. Death Cross Sell.

# BarUpDn: 
if open[i] > close[i-1], close[i-1] > open[i-1] enter long
if open[i] < close[i-1], close[i-1] < open[i-1] enter short

# OutSideBar:
if low[i] < low[i-1], high[i] > high[i-1] 
red bar sell, green bar buy

# Slow&FastSMA:
If not in position and FastSMA > SLOWSMA ->BUY
If in position and SlowSMA > FastSMA -> Sell
