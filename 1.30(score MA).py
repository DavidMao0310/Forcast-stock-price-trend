import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('ggplot')
import talib as ta

data = pd.read_csv('dataset/TSLA (30:01:21).csv')
pd.set_option('display.max_columns', None)
data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
data.set_index('Date', inplace=True)
data['1d_back_close'] = data['Adj_Close'].shift(1)
data['1d_close_pct'] = data['Adj_Close'].pct_change(1)
feature_names = []
dummies = []
for n in [8, 13, 21, 34]:
    data['ema' + str(n)] = ta.EMA(data['Adj_Close'].values, timeperiod=n)
    feature_names = feature_names + ['ema' + str(n)]

for n in [55, 89, 144, 233]:
    data['sma' + str(n)] = ta.SMA(data['Adj_Close'].values, timeperiod=n)
    feature_names = feature_names + ['sma' + str(n)]

data.dropna(inplace=True)


def get_score(n):
    list = []
    for i in range(len(data[str(n)])):
        if data['Adj_Close'][i] > data[str(n)][i]:
            list.append(1)
        elif data['Adj_Close'][i] < data[str(n)][i]:
            list.append(-1)
        else:
            list.append(0)
    data['dum_' + str(n)] = np.array(list)


for n in feature_names:
    get_score(n)
    dummies = dummies + ['dum_' + str(n)]

get_score('1d_back_close')
print(data)

for n in dummies:
    plt.plot(data.index, np.cumsum(data[str(n)].values), label=str(n))
    print('total_' + str(n) + '=', np.cumsum(data[str(n)].values)[-1])
plt.legend()
plt.title('score step change')
plt.show()

data['Adj_Close'].plot()
for i in feature_names:
    data[str(i)].plot()
plt.title('indicator values')
plt.legend()
plt.show()
