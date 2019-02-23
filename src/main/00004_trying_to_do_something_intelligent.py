import numpy as np

import src.service.date_helper as date_helper
import src.service.file_io_service as file_io_service
import src.strategy.buy_and_hold_strategy as buy_and_hold_strategy
import src.strategy.macd_strategy as macd_strategy
import src.strategy.rsi_and_macd_strategy as rsi_and_macd_strategy
import src.strategy.rsi_strategy as rsi_strategy


def main():
    file_content = file_io_service.load_file('PETR4.SA')
    file_content = file_content.dropna()

    close = file_content['Adj Close'].values
    date = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    print('lucro com buy and hold: ' + str(buy_and_hold_strategy.execute(date, close)))
    print('lucro com macd: ' + str(macd_strategy.execute(date, close)))
    print('lucro com rsi: ' + str(rsi_strategy.execute(date, close)))
    print('lucro com rsi e macd: ' + str(rsi_and_macd_strategy.execute(date, close)))


if __name__ == '__main__':
    main()
