import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Inspiration: https://levelup.gitconnected.com/an-algo-trading-strategy-which-made-8-371-a-python-case-study-58ed12a492dc

#Rules:
#Buy = current high > 50 week high
#Sell = current low < 40 week low

data = pd.read_csv('DCI_strategy_data.csv')

def buy_sell(data):
    flag = 0
    buy = []
    sell = []
    open_pos = []
    funds = [10000]*len(data)
    last_funds = 10000
    end_of_year_bal = [last_funds]

    for i in range(0, len(data)):
        curr_high = data['high'][i]
        curr_low = data['low'][i]
        curr_price = data['price'][i]        
        #Case 1: curr_high > upper_channel = Buy
        if curr_high == data['upper_channel'][i]:
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
        #Case 2: curr_low < lower_channel = SelL
        elif curr_low == data['lower_channel'][i]:
            #Case 2A: above to below
            if flag == 1:
                flag = 0
                buy.append(np.NaN)
                sell.append(curr_price)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                # print(funds[i])
                open_pos.append(0)
            #Case 2B: below and still below
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                funds[i] = last_funds
                open_pos.append(0)
        #In the first 49 days before we have both channels, we have a base case, (Also when either case is not hit)
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
    print('Original funds: ' + str(data['funds_track'][0]) + '\n')
    print('Outcome funds: ' + str(data['funds_track'][len(data)-1]) + '\n')
    print('profit = ' + str(data['funds_track'][len(data)-1] - data['funds_track'][0]))
    
    #Calculating yoy %change
    res = []
    for i in range(1, len(bals)):
        currYearprof_loss = ((bals[i] - bals[i-1])/bals[i-1]) * 100
        res.append(currYearprof_loss)
    print('YoY pct_change = '  + str(sum(res)/len(res)))

    # Visualize Data and strategy to buy and sell
    plt.figure(figsize = (15, 8))
    plt.plot(data['price'], label = 'MSFT', linewidth = 1)
    plt.plot(data['upper_channel'], label = 'Upper Channel', linewidth = 0.5)
    plt.plot(data['lower_channel'], label = 'Lower Channel', linewidth = 0.5)

    plt.scatter(data.index, data['buy_signal'], label= 'Buy', marker = '^', color = 'g')
    plt.scatter(data.index, data['sell_signal'], label= 'Sell', marker = 'v', color = 'r')
    plt.title('MSFT' + ' Buy-Sell Signals')
    plt.xlabel('Stock History over 30 years')
    plt.ylabel('Adjusted Close price ($)')
    plt.legend(loc = 'upper left')
    plt.show()

if __name__ == "__main__":
    main()