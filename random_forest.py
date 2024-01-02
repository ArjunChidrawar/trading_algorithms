import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss

#Making prediction variable (if tomorrow's closing is greater than today's closing, set to 1 = buy , else 0 = sell)
def make_output(data):
    buys_sells = [-1]
    for i in range(len(data)-1):
        if data['price'][i+1] > data['price'][i]:
            buys_sells.append(1)
        else:
            buys_sells.append(-1)
    return buys_sells

def accuracy(Y, Yhat):
    correct = 0
    for i in range(len(Y)):
        if Y[i] == Yhat[i]:
            correct += 1
    return correct/len(Y)

#Making indicators for graph
def graph_converts(data):
    buy = [np.NaN]
    sell = [np.NaN]
    open_pos = [0]
    last_pos = 10000/data['price'][0]
    funds = [10000]*len(data)
    last_funds = 10000
    end_of_year_bal = []

    for i in range(1, len(data)):
        curr_price = data['price'][i]
        #buy case
        if ((data['buy_sell'][i] == 1) and (data['buy_sell'][i-1] == -1)):
            buy.append(data['price'][i])
            sell.append(np.NaN)
            last_pos = last_funds/curr_price
            funds[i] = last_funds
            open_pos.append(last_pos)
        #sell case
        elif ((data['buy_sell'][i] == -1) and (data['buy_sell'][i-1] == 1)):
            buy.append(np.NaN)
            sell.append(data['price'][i])
            last_funds = last_pos*curr_price
            funds[i] = last_funds
            open_pos.append(0)
        #holding or staying exited
        else:
            buy.append(np.NaN)
            sell.append(np.NaN)
            if data['buy_sell'][i] == 1:
                last_funds = last_pos*curr_price
                funds[i] = last_funds
                open_pos.append(last_pos)
            else:
                open_pos.append(0)
        date_format = '%Y-%m-%d %H:%M:%S%z'
        date_obj = datetime.strptime(data['Date'][i], date_format)
        date_obj2 = datetime.strptime(data['Date'][i-1], date_format)
        if date_obj.year != date_obj2.year :
            end_of_year_bal.append(funds[i-1])
    return buy, sell, funds, end_of_year_bal



def main():
    data = pd.read_csv('feature_data.csv')
    
    #Making buy_sell outputs
    outputs = make_output(data)
    data['buy_sell'] = outputs

    data = data.iloc[49:]
    data.reset_index(drop=True, inplace=True)
    #Making X matrix and Y prediction variable
    Xmat = data.drop(columns=['Date', 'buy_sell']).to_numpy(dtype=np.float64)
    Y = data['buy_sell'].to_numpy(dtype=np.float64)

    #Splitting into train, test (80% train, 10% val, 10% test)
    Xmat_train, Xmat_val, Y_train, Y_val = train_test_split(Xmat, Y, test_size=0.1, random_state=4)
    Xmat_train, Xmat_test, Y_train, Y_test = train_test_split(Xmat_train, Y_train, test_size=0.11111111111, random_state=4)
    n, d = Xmat_train.shape

    model = RandomForestClassifier(n_estimators = 100, random_state = 4)
    model.fit(Xmat_train, Y_train)

    Yhat = model.predict(Xmat_val)

    logLoss = log_loss(Y_val, Yhat)
    acc = accuracy(Y_val, Yhat)
    print(f'Cross_entropy_loss = {logLoss} \n')
    print(f'Accuracy = {acc}')

    #Making Visualizations
    inds = graph_converts(data)
    data['buy_signal'] = inds[0]
    data['sell_signal'] = inds[1]
    data['funds_track'] = inds[2]
    bals = inds[3]

    print('Original funds: ' + str(data['funds_track'][49]) + '\n')
    print('Outcome funds: ' + str(data['funds_track'][len(data)-1]) + '\n')
    print('profit = ' + str(data['funds_track'][len(data)-1] - data['funds_track'][49]))

    #Calculating yoy %change
    res = []
    for i in range(len(bals)-1):
        currYearprof_loss = ((bals[i+1] - bals[i])/bals[i]) * 100
        res.append(currYearprof_loss)
    print('YoY pct_change = '  + str(sum(res)/len(res)))

    plt.figure(figsize = (15, 8))
    plt.plot(data['price'], label = 'MSFT', linewidth = 1)

   
    plt.scatter(data.index, data['buy_signal'], label= 'Buy', marker = '^', color = 'g')
    plt.scatter(data.index, data['sell_signal'], label= 'Sell', marker = 'v', color = 'r')
    plt.title('MSFT' + ' Buy-Sell Signals')
    plt.xlabel('Stock History over 10 years')
    plt.ylabel('Adjusted Close price ($)')
    plt.legend(loc = 'upper left')
    plt.show()
    

if __name__ == "__main__":
    main()