import pandas as pd
import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')



#Initial Cleaning (Taking data from the last 5 years)
data = pd.read_csv('MSFT.csv')
data.dropna(inplace=True)

#Initial stock data Visualization
plt.figure(figsize=(15, 8))
plt.plot(data['Adj Close'], label = 'MSFT', linewidth = 0.5)
plt.title('Adjusted close price history')
plt.xlabel('Previous 5 years')
plt.ylabel('Adj. close price ($)')
plt.legend(loc = 'upper left')
plt.show()


#Creating Simple Moving Averages (20 days, 50 days)
SMA20 = pd.DataFrame()
SMA20['vals'] = data['Adj Close'].rolling(window= 20).mean()

SMA50 = pd.DataFrame()
SMA50['vals'] = data['Adj Close'].rolling(window = 50).mean()

df = pd.DataFrame()
df['price'] = data['Adj Close']
df['SMA20'] = SMA20['vals']
df['SMA50'] = SMA50['vals']
df['live_pos'] = 100000

df.to_csv('data_for_strategy.csv')


