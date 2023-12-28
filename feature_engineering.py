import pandas as pd
import numpy as np


data = pd.read_csv('MSFT.csv')
sma = pd.read_csv('data_for_SMA.csv')

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
    data['Middle Band'] = sma['SMA20']
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
    

# def stochastic_oscillator(data):
# def compute KAMA(data):
# def compute_ATR(data):
# def compute_vroc(data):
# def compute_volatility(data):
# def compute_DMI(data):

def main():
    fdata = pd.DataFrame()

    #price
    fdata['price'] = data['Close']

    #RSI
    fdata['RSI'] = compute_rsi(data)

    #bollinger bands
    bollinger_bds = bollinger_bands(data)
    fdata['upper_band'] = bollinger_bds[0]
    fdata['lower_band'] = bollinger_bds[1]
    fdata['middle_band'] = sma['SMA20']

    #MACD
    inds = compute_MACD(data)
    fdata['MACD_line'] = inds[0]
    fdata['signal_line'] = inds[1]
    
    #beta_value
    beta_val = compute_beta(data)
    print(beta_val)

    fdata.to_csv('test.csv')
    
if __name__ == "__main__":
    main()

