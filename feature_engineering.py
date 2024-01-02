import pandas as pd
import numpy as np


#Base stock data
data = pd.read_csv('MSFT.csv')

#Needed for bollinger bands
sma = pd.read_csv('data_for_SMA.csv')

#Needed for Donchian Channels
weekly = pd.read_csv('weekly_MSFT.csv')

#Computing RSI (Relative Strength Index)
def compute_rsi(data):
    df = pd.DataFrame()
    #Step 1: calculating price changes between each day
    df['price_changes'] = data['Close'].diff()

    #Step 2: Separating daily gains and losses 
    df['only_gain'] = df['price_changes'].apply(lambda x: max(0, x))
    df['only_loss'] = -df['price_changes'].apply(lambda x: min(0, x))

    #Step 3: Calculating average gain and average loss over past 14 days
    data['avg_gain'] = df['only_gain'].rolling(window = 14).mean()
    data['avg_loss'] = df['only_loss'].rolling(window = 14).mean()

    #Step 4: Implement RSI calculation (100 - (100/(1+RS)))
    #RS = Average Gain/ Average Loss
    RSI = []
    for i in range(len(data['avg_gain'])):
        RS = (data['avg_gain'][i]/data['avg_loss'][i])
        RSI.append(100 - (100/(1 + RS)))
    return RSI

#Need standard deviation and 20 day SMA to compute bollinger bands
def bollinger_bands(data):
    data['Middle Band'] = data['Close'].rolling(window = 20).mean()
    data['rolling_std_dev'] = data['Close'].rolling(window = 20).std()
    Upper_Band = data['Middle Band'] + (2*data['rolling_std_dev'])
    Lower_Band = data['Middle Band'] - (2*data['rolling_std_dev'])
    return Upper_Band, Lower_Band

#Computing Moving Average Convergence/Divergence (Good for analyzing larger price trends)
def compute_MACD(data):
    df = pd.DataFrame()
    #First compute MACD line (12 day EMA - 26 day EMA)
    df['EMA12'] = data['Close'].ewm(span = 12, adjust = False).mean()
    df['EMA26'] = data['Close'].ewm(span = 26, adjust = False).mean()
    df['MACD_line'] = df['EMA12'] - df['EMA26']
    MACD_line = df['MACD_line']

    #Compute signal line (9 day EMA)
    df['signal_line'] = df['MACD_line'].ewm(span = 9, adjust = False).mean()
    signal_line = df['signal_line']

    #Adding the optional histogram for better visualization
    histogram = df['signal_line'] - df['MACD_line']

    return MACD_line, signal_line, histogram

#IN PROGRESS
def compute_ADX(data, period = 14):
    df = pd.DataFrame()
    df['high-low'] = data['high'] - data['low']
    df['high-prevClose'] = abs(data['high'] - data['Close'].shift(1))
    df['low-prevClose'] = abs(data['low'] - data['Close'].shift(1))

    #Calculating True Range: max(high-low, |high-prev_close|, |low-prev_close|)
    df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

def compute_beta(data):    
    df = pd.read_csv('SNP.csv')
    df = df.dropna(axis = 0)
    combined_data = pd.merge(df, data, on = 'Date', suffixes = ('_market', '_stock'))
    combined_data['return_stock'] = combined_data['Close_stock'].pct_change() * 100 
    combined_data['return_market'] = combined_data['Close_market'].pct_change() * 100
    covariance = combined_data['return_stock'].cov(combined_data['return_market'])
    
    variance_market = combined_data['return_market'].var()

    beta = covariance/variance_market
    return beta

#NOTE: this indicator uses weekly data instead of daily
def compute_donchian_channels(data):
    highs = data['High'].rolling(window = 50).max()
    lows = data['Low'].rolling(window = 40).min()
    return highs, lows

def compute_ATR(data):
    df = pd.DataFrame()
    df['high-low'] = data['High'] - data['Low']
    df['high-prevClose'] = abs(data['High'] - data['Close'].shift(1))
    df['low-prevClose'] = abs(data['Low'] - data['Close'].shift(1))

    #Calculating True Range: max(high-low, |high-prev_close|, |low-prev_close|)
    df['TR'] = df[['high-low', 'high-prevClose', 'low-prevClose']].max(axis=1)
    ATR = df['TR'].rolling(window = 14).mean()
    return ATR

def compute_volumeMA(data):
    volumeMA = data['Volume'].rolling(window = 14).mean()
    return volumeMA

# def stochastic_oscillator(data):
# def compute KAMA(data):
# def compute_vroc(data):
# def compute_DMI(data):

def main():
    fdata = pd.DataFrame()

    #adding dates
    fdata['Date'] = data['Date']

    #percentage change
    fdata['pct_change'] = data['Close'].pct_change(periods = 1)

    #volume
    fdata['Volume'] = data['Volume']

    #simple moving average (50 days)
    fdata['SMA50'] = sma['SMA50']

    #price
    fdata['price'] = data['Close']

    #RSI
    fdata['RSI'] = compute_rsi(data)

    #bollinger bands (middle band is 20 day SMA)
    bollinger_bds = bollinger_bands(data)
    fdata['upper_band'] = bollinger_bds[0]
    fdata['lower_band'] = bollinger_bds[1]
    fdata['middle_band'] = data['Middle Band']

    #MACD
    inds = compute_MACD(data)
    fdata['MACD_line'] = inds[0]
    fdata['signal_line'] = inds[1]
    
    #beta_value
    beta_val = compute_beta(data)

    #average true range (volatility indicator)
    ATR = compute_ATR(data)
    fdata['ATR'] = ATR
    
    #volume moving average
    volumeMA = compute_volumeMA(data)
    fdata['volume_ma'] = volumeMA

    #Donchian Channels (period is different so we use a different dataset)
    wdata = pd.DataFrame()
    DCI = compute_donchian_channels(weekly)
    wdata['Date'] = weekly['Date']
    wdata['price'] = weekly['Close']
    wdata['upper_channel'] = DCI[0]
    wdata['lower_channel'] = DCI[1]
    wdata['high'] = weekly['High']
    wdata['low'] = weekly['Low']
    
    wdata.to_csv('DCI_strategy_data.csv')

    fdata.to_csv('feature_data.csv')
    
if __name__ == "__main__":
    main()

