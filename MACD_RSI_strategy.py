import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


data = pd.read_csv('test.csv')

#Idea for this strategy:
#Buy Signal: RSI <= 30 AND MACD crosses to above signal line
#Sell Signal: RSI >= 70 AND MACD crosses to below signal line
#Strategy Reasoning: This strategy creates a more robust signal, indicating price 
#trend and momentum match the same direction and reduces losses on false signals

def buy_sell(data):
    flag = 0
    buy = []
    sell = []
    open_pos = []
    funds = [10000]*len(data)
    last_funds = 10000
    
    for i in range(len(data)):
        curr_price = data['price'][i]
        #Case 1: Buy
        if (data['MACD_line'][i] > data['signal_line'][i]) and (data['RSI'][i] <= 30):
            #Case 1A: going from sell to buy
            if flag == 0:
                flag = 1
                buy.append(curr_price)
                sell.append(np.NaN)
                last_pos = last_funds/curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            #Case 1B: stay in buy
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
        #Case 2: SMA20 < SMA50
        elif (data['MACD_line'][i] < data['signal_line'][i]) and (data['RSI'][i] >= 70):
            #Case 2A: going from buy to sell
            if flag == 1:
                flag = 0
                buy.append(np.NaN)
                sell.append(curr_price)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(0)
            #Case 2B: stay in sell
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                funds[i] = last_funds
                open_pos.append(0)
        else:
            if flag == 1:
                buy.append(np.NaN)
                sell.append(np.NaN)
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            else:
                buy.append(np.NaN)
                sell.append(np.NaN)
                funds[i] = last_funds
                open_pos.append(0)
                
    return buy, sell, open_pos, funds

def main():
    indicators = buy_sell(data)
    data['buy_signal'] = indicators[0]
    data['sell_signal'] = indicators[1]
    data['open_position'] = indicators[2]
    data['funds_track'] = indicators[3]

    #Outcome value for funds:
    print('Original funds: ' + str(data['funds_track'][49]) + '\n')
    print('Outcome funds: ' + str(data['funds_track'][len(data)-1]) + '\n')
    print('profit/loss = ' + str(data['funds_track'][len(data)-1] - data['funds_track'][49]))

    plt.figure(figsize = (15, 8))
    #plt.plot(data['price'], label = 'MSFT', linewidth = 1)
    plt.plot(data['MACD_line'], label = 'MACD_Line', linewidth = 0.5)
    plt.plot(data['signal_line'], label = 'Signal Line', linewidth = 0.5)

    plt.scatter(data.index, data['buy_signal'], label= 'Buy', marker = '^', color = 'g')
    plt.scatter(data.index, data['sell_signal'], label= 'Sell', marker = 'v', color = 'r')
    plt.title('MSFT' + ' Buy-Sell Signals')
    plt.xlabel('Stock History over 1000 Days')
    plt.ylabel('Adjusted Close price ($)')
    plt.legend(loc = 'upper left')
    plt.show()

if __name__ == "__main__":
    main()