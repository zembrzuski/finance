import numpy as np

import src.service.date_helper as date_helper
import src.service.file_io_service as file_io_service
import src.strategy.buy_and_hold_strategy as buy_and_hold_strategy
import src.strategy.macd_strategy as macd_strategy
import src.strategy.rsi_and_macd_strategy as rsi_and_macd_strategy
import src.strategy.rsi_strategy as rsi_strategy
import src.service.period_sampler_service as period_sampler_service


def main():
    file_content = file_io_service.load_file('PETR4.SA')
    file_content = file_content.dropna()

    prices = file_content['Adj Close'].values
    dates = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    dates, prices = period_sampler_service.do_single_sampling(dates, prices)

    print('lucro com buy and hold: ' + str(buy_and_hold_strategy.execute(dates, prices)))
    print('lucro com macd: ' + str(macd_strategy.execute(dates, prices)))
    print('lucro com rsi: ' + str(rsi_strategy.execute(dates, prices)))
    print('lucro com rsi e macd: ' + str(rsi_and_macd_strategy.execute(dates, prices)))


if __name__ == '__main__':
    main()
