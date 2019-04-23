import numpy as np
from talib import RSI, MACD
import src.service.file_io_service as file_io_service


def get_labeled_quotes(company_code):
    dates, prices = file_io_service.get_historical_data(company_code)

    my_dataframe = np.transpose(np.concatenate(([dates], [prices]), axis=0))
    labeled_quotes = np.hstack((my_dataframe, np.transpose([np.append(my_dataframe[:, 1][1:], 0)])))
    labeled_quotes = labeled_quotes[0:-1, :]

    return labeled_quotes


def create_lots_of_rsis(prices):
    rsis = np.reshape(RSI(prices, timeperiod=6), (len(prices), 1))

    for i in range(7, 21):
        rsi_i = np.reshape(RSI(prices, timeperiod=i), (len(prices), 1))
        rsis = np.hstack((rsis, rsi_i))

    print('oi')
    return rsis


def main():
    company_code = 'PETR4.SA'
    labeled_quotes = get_labeled_quotes(company_code)

    prices = np.array([float(x) for x in labeled_quotes[:, 1]])
    # rsi = RSI(prices, timeperiod=14)
    # macd, macdsignal, macdhist = MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    create_lots_of_rsis(prices)

    # proximo passo: colocar na minha matriz uma penca grotesca de indicadores

    print('finished')


if __name__ == '__main__':
    main()
