import src.service.file_io_service as file_io_service
import src.service.date_helper as date_helper
import matplotlib.pyplot as plt
import numpy as np
from talib import RSI, BBANDS, MACD

def main():
    file_content = file_io_service.load_historical_data('PETR4.SA')
    file_content = file_content.dropna()

    close = file_content['Adj Close'].values
    date = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    rsi = RSI(close, timeperiod=14)
    macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    fig, (ax0, ax1, ax2) = plt.subplots(3, 1, sharex=True, figsize=(12, 8))
    ax0.plot(date, close, label='Close')
    ax0.set_xlabel('Date')
    ax0.set_ylabel('Close')
    ax0.grid()

    ax1.plot(date, rsi, label='Close', linewidth=.5)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close')
    ax1.grid()

    ax2.plot(date, up, label='BB_up', color='BLUE', linewidth=.5)
    ax2.plot(date, close, label='AdjClose', color='BLACK', linewidth=.5)
    ax2.plot(date, low, label='BB_low', color='RED', linewidth=.5)
    ax2.fill_between(date, y1=low, y2=up, color='#adccff', alpha='0.3')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Bollinger Bands')
    ax2.grid()

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
