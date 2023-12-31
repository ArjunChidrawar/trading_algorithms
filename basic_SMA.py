import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

data = pd.read_csv('data_for_SMA.csv')

# Defined Rules for Strategy:
# 1. Buy = SMA20 goes from less than SMA 50 to greater
# 2. Sell = SMA20 goes from greater than SMA 50 to less
# 3. open position = our current money value divided by the price of the stock (gives us the number of shares we have invested)
# flag is used to tell if we went from above to below or below to above
def buy_sell(data):
    flag = 0
    buy = []
    sell = []
    open_pos = []
    funds = [10000]*len(data)
    last_funds = 10000
    end_of_year_bal = []

    for i in range(len(data)):
        curr_price = data['price'][i]
        #Case 1: SMA20 > SMA50
        if data['SMA20'][i] > data['SMA50'][i]:
            #Case 1A: below to above
            if flag == 0:
                flag = 1
                buy.append(curr_price)
                sell.append(np.NaN)
                last_pos = last_funds/curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            #Case 1B: above and still above
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
        #Case 2: SMA20 < SMA50
        elif data['SMA20'][i] <= data['SMA50'][i]:
            #Case 2A: above to below
            if flag == 1:
                flag = 0
                buy.append(np.NaN)
                sell.append(curr_price)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(0)
            #Case 2B: below and still below
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                funds[i] = last_funds
                open_pos.append(0)
        #In the first 49 days before we have both SMA's, we have a base case
        else:
            buy.append(np.NaN)
            sell.append(np.NaN)
            open_pos.append(0)
        #For calculating YoY revenues
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
    data.to_csv('test.csv')
    #Outcome value for funds:
    print('Original funds: ' + str(data['funds_track'][49]) + '\n')
    print('Outcome funds: ' + str(data['funds_track'][len(data)-1]) + '\n')
    print('profit = ' + str(data['funds_track'][len(data)-1] - data['funds_track'][49]))

    #Calculating yoy %change
    res = []
    for i in range(len(bals)-1):
        currYearprof_loss = ((bals[i+1] - bals[i])/bals[i]) * 100
        res.append(currYearprof_loss)
    print('YoY pct_change = '  + str(sum(res)/len(res)))

    # Visualize Data and strategy to buy and sell
    plt.figure(figsize = (15, 8))
    plt.plot(data['price'], label = 'MSFT', linewidth = 1)
    plt.plot(data['SMA20'], label = 'SMA20', linewidth = 0.5)
    plt.plot(data['SMA50'], label = 'SMA50', linewidth = 0.5)
   
    plt.scatter(data.index, data['buy_signal'], label= 'Buy', marker = '^', color = 'g')
    plt.scatter(data.index, data['sell_signal'], label= 'Sell', marker = 'v', color = 'r')
    plt.title('MSFT' + ' Buy-Sell Signals')
    plt.xlabel('Stock History over 10 years')
    plt.ylabel('Adjusted Close price ($)')
    plt.legend(loc = 'upper left')
    plt.show()

if __name__ == "__main__":
    main()