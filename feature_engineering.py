import pandas as pd
import numpy as np


data = pd.read_csv('MSFT.csv')
sma = pd.read_csv('data_for_SMA.csv')

#Computing RSI (Relative Strength Index)
def compute_rsi(data):
    df = pd.DataFrame()
    #Step 1: calculating price changes between each day
    df['price_changes'] = data['Adj Close'].diff()

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
    data['rolling_std_dev'] = data['Adj Close'].rolling(window = 20).std()
    Upper_Band = data['Middle Band'] + (2*data['rolling_std_dev'])
    Lower_Band = data['Middle Band'] - (2*data['rolling_std_dev'])
    return Upper_Band, Lower_Band
    
# def stochastic_oscillator(data):
# def compute_beta(data):
# def compute_vroc(data):
# def compute_volatility(data):
# def compute_MACD(data):
# def compute_DMI(data):

def main():
    
    fdata = pd.DataFrame()

    #price
    fdata['price'] = data['Adj Close']

    #RSI
    fdata['RSI'] = compute_rsi(data)

    #bollinger bands
    bollinger_bds = bollinger_bands(data)
    fdata['upper_band'] = bollinger_bds[0]
    fdata['lower_band'] = bollinger_bds[1]
    fdata['middle_band'] = sma['SMA20']


    fdata.to_csv('test.csv')
    
if __name__ == "__main__":
    main()

