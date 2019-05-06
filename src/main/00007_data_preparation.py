import numpy as np
from talib import RSI, MACD, BBANDS
import src.service.file_io_service as file_io_service
import src.service.date_helper as date_helper
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split


def get_labeled_quotes(company_code):
    historical_data = file_io_service.read_csv(company_code)

    dates = np.array(list(map(lambda x: pd.Timestamp(x, tz=None), historical_data['Date'])))

    historical_data = historical_data.assign(Datee=pd.Series(dates))

    next_day_close = np.array(historical_data['Adj Close'][1:])
    next_day_close = np.append(next_day_close, -1)

    historical_data = historical_data.assign(Next_Day_Close=pd.Series(next_day_close))
    historical_data = historical_data.drop([historical_data.shape[0]-1])

    label = (historical_data['Next_Day_Close'] - historical_data['Adj Close'] > 0).apply(int)
    historical_data = historical_data.assign(label=pd.Series(label))

    return historical_data


def add_rsi(historical_data):
    prices = historical_data['Adj Close'].as_matrix()

    rsis = dict()

    for i in range(6, 21):
        rsi_i = RSI(prices, timeperiod=i)
        rsis['rsi' + str(i)] = rsi_i

    rsis_dataframe = pd.DataFrame(rsis)

    return historical_data.join(rsis_dataframe)


def main():
    print('init data preparation')
    company_code = 'PETR4.SA'

    historical_data = get_labeled_quotes(company_code)
    historical_data = add_rsi(historical_data)

    # print(historical_data['label'].value_counts())
    # sns.countplot(x='label', data=historical_data, palette='hls')
    # plt.show()
    # historical_data.groupby('label').mean()

    y = historical_data['label']
    X = historical_data.drop(columns=['label', 'Next_Day_Close'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


    print('finished')


if __name__ == '__main__':
    main()
