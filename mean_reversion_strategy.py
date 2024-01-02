import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

data = pd.read_csv('feature_data.csv')
#Using bollinger bands for buy/sell signal

#RULES:
# BUY = price < lower band AND RSI < 30
# SELL = price > upper band AND RSI > 70
# REASONING: bollinger bands indicate momentum, so if price goes above upper band, it indicates overbought
# if price goes below lower band it indicates underbought. RSI does the same thing with a metric between 0 and 100,
# so by using both we minimize false signals
# curr profit = $21,018.57
def buy_sell(data):
    flag = 0
    buy = []
    sell = []
    open_pos = []
    funds = [10000]*len(data)
    last_funds = 10000
    end_of_year_bal = [last_funds]

    for i in range(len(data)):
        curr_price = data['price'][i]
        #Case 1: price < lower band = buy
        if data['price'][i] <= data['lower_band'][i] and data['RSI'][i] < 30:
            #Case 1A: above to below
            if flag == 0:
                flag = 1
                buy.append(curr_price)
                sell.append(np.NaN)
                last_pos = last_funds/curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            #Case 1B: below and still below
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
        #Case 2: price > upper band = sell
        elif (data['price'][i] >= data['upper_band'][i]) and data['RSI'][i] > 70:
            #Case 2A: above to below
            if flag == 1:
                flag = 0
                buy.append(np.NaN)
                sell.append(curr_price)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(0)
            #Case 2B: above and still above
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                funds[i] = last_funds
                open_pos.append(0)
        #When we are between the two bollinger bands
        else:
            buy.append(np.NaN)
            sell.append(np.NaN)
            if flag == 1:
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            else:
                funds[i] = last_funds
                open_pos.append(0)
        date_format = '%Y-%m-%d %H:%M:%S%z'
        if i+1 != len(data):
            date_obj = datetime.strptime(data['Date'][i], date_format)
            date_obj2 = datetime.strptime(data['Date'][i+1], date_format)
            if date_obj.year != date_obj2.year :
                end_of_year_bal.append(funds[i])
        
    return buy, sell, open_pos, funds, end_of_year_bal

def main():
    indicators = buy_sell(data)
    data['buy_signal'] = indicators[0]
    data['sell_signal'] = indicators[1]
    data['open_position'] = indicators[2]
    data['funds_track'] = indicators[3]
    bals = indicators[4]

    #Outcome value for funds:
    print('Original funds: ' + str(data['funds_track'][49]) + '\n')
    print('Outcome funds: ' + str(data['funds_track'][len(data)-1]) + '\n')
    profit = data['funds_track'][len(data)-1] - data['funds_track'][49]
    print('profit = ' + str(profit))
    
    #Calculating yoy %change
    res = []
    for i in range(1, len(bals)):
        currYearprof_loss = ((bals[i] - bals[i-1])/bals[i-1]) * 100
        res.append(currYearprof_loss)
    print('YoY pct_change = '  + str(sum(res)/len(res)))

    # Visualize Data and strategy to buy and sell
    plt.figure(figsize = (15, 8))
    plt.plot(data['price'], label = 'MSFT', linewidth = 1)
    plt.plot(data['upper_band'], label = 'Upper Band', linewidth = 0.5)
    plt.plot(data['lower_band'], label = 'Lower Band', linewidth = 0.5)
    #plt.plot(data['live_pos'], label = 'live position', linewidth = 0.5)
    plt.scatter(data.index, data['buy_signal'], label= 'Buy', marker = '^', color = 'g')
    plt.scatter(data.index, data['sell_signal'], label= 'Sell', marker = 'v', color = 'r')
    plt.title('MSFT' + ' Buy-Sell Signals')
    plt.xlabel('Stock History over 10 years')
    plt.ylabel('Adjusted Close price ($)')
    plt.legend(loc = 'upper left')
    plt.show()
    
if __name__ == "__main__":
    main()