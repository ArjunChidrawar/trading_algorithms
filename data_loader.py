import pandas as pd
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#Getting S&P 500 data
snp_data = yf.Ticker('^GSPC')
snp = snp_data.history(period='1d', start='2013-1-1', auto_adjust= True)
snp.to_csv('SNP.csv')

#Getting Stock data: 'MSFT' for now
ticker_symbol = 'MSFT'
ticker_data = yf.Ticker(ticker_symbol)
data = ticker_data.history(period = '1d', start='2013-1-1', auto_adjust= True)
data.to_csv('MSFT.csv')

#Getting weekly stock data (starting 1993 here for more data)
ticker_symbol = 'MSFT'
ticker_data = yf.Ticker(ticker_symbol)
wdata = ticker_data.history(period = '1w', start='1993-1-1', auto_adjust= True)
wdata.to_csv('weekly_MSFT.csv')

#Initial Cleaning (Taking data from the last 10 years)
#data = pd.read_csv('MSFT.csv')
data.dropna(inplace=True)
wdata.dropna(inplace = True)

#Initial stock data Visualization
plt.figure(figsize=(15, 8))
plt.plot(data['Close'], label = 'MSFT', linewidth = 0.5)
plt.title('Close price history')
plt.xlabel('Previous 10 years')
plt.ylabel('Close price ($)')
plt.legend(loc = 'upper left')
plt.show()


#Creating Simple Moving Averages (20 days, 50 days)
SMA20 = pd.DataFrame()
SMA20['vals'] = data['Close'].rolling(window= 20).mean()

SMA50 = pd.DataFrame()
SMA50['vals'] = data['Close'].rolling(window = 50).mean()

df = pd.DataFrame()
df['price'] = data['Close']
df['SMA20'] = SMA20['vals']
df['SMA50'] = SMA50['vals']
df['live_pos'] = 100000

df.to_csv('data_for_SMA.csv')


