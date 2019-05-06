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
from sklearn.metrics import confusion_matrix as confusion


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


def create_lots_of_macds(historical_data):
    prices = historical_data['Adj Close'].as_matrix()

    all_macds = dict()

    for fast_period in range(9, 16):
        for slow_period in range(20, 31):
            for signal_period in range(5, 12):
                macd, macdsignal2, macdhist = MACD(
                    prices,
                    fastperiod=fast_period,
                    slowperiod=slow_period,
                    signalperiod=signal_period
                )

                all_macds['macd_{}_{}_{}'.format(fast_period, slow_period, signal_period)] = macdsignal2

    macds_dataframe = pd.DataFrame(all_macds)

    return historical_data.join(macds_dataframe)


def create_bollinger_bands(historical_data):
    prices = historical_data['Adj Close'].as_matrix()

    bollinger_bands = dict()

    for time_period in range(10, 31):
        for up in range(18, 23):
            for down in range(18, 23):
                upper, middle, lower = BBANDS(
                    prices,
                    timeperiod=time_period,
                    nbdevup=float(up)/10,
                    nbdevdn=float(down)/10,
                    matype=0)

                bollinger_bands['bbands_upper_{}_{}_{}'.format(time_period, up, down)] = upper/prices
                bollinger_bands['bbands_lower_{}_{}_{}'.format(time_period, up, down)] = lower/prices

    macds_dataframe = pd.DataFrame(bollinger_bands)

    return historical_data.join(macds_dataframe)


def main():
    print('init data preparation')

    company_code = 'BBAS3.SA'
    # company_code = 'PETR4.SA'

    historical_data = get_labeled_quotes(company_code)
    historical_data = add_rsi(historical_data)
    historical_data = create_lots_of_macds(historical_data)
    historical_data = create_bollinger_bands(historical_data)

    historical_data = historical_data.dropna()
    historical_data = historical_data.reset_index(drop=True)

    # print(historical_data['label'].value_counts())
    # sns.countplot(x='label', data=historical_data, palette='hls')
    # plt.show()
    # historical_data.groupby('label').mean()

    y = historical_data['label']
    X = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    # X = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)

    print('Accuracy of logistic regression classifier on train set: {:.2f}'.format(logreg.score(X_train, y_train)))
    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

    confusion_matrix = confusion(y_test, y_pred)
    print(confusion_matrix)

    print('finished')


if __name__ == '__main__':
    main()
