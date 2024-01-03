# trading_algorithms
I completed this personal project to learn trading strategy and algorithmic trading

Implemented 3 rules based strategies:

1. Basic SMA -- Simple Moving Average Strategy
   Rules:
     Buy = 20 day SMA > 50 day SMA
     Sell = 20 day SMA < 50 day SMA
2. Mean Reversion Strategy -- Bollinger Bands and Relative Strength Index
   Rules:
     Buy = price < lower band AND RSI < 30
     Sell = price > upper band AND RSI > 70
3. Donchian Channels Strategy -- Longer-term strategy using Weekly data
   Rules:
     Buy = current high > 50 week high
     Sell = current low < 50 week low

I also implemented a random forest algorithm: (random_forest.py)
For my random forest, I converted the strategy into a classification problem (BUY or SELL).
Check "feature_engineering.py" for the full list of features I used.
