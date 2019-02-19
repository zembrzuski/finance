import service.file_io_service as file_io_service
import service.date_helper as date_helper
import numpy as np
import strategy.buy_and_hold_strategy as buy_and_hold
import strategy.macd_strategy as macd_strategy
import service.trade_helper as trade_helper
import pprint


def main():
    file_content = file_io_service.load_file('PETR4.SA')
    file_content = file_content.dropna()

    close = file_content['Adj Close'].values
    date = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    trades = buy_and_hold.execute(date, close)
    profit = list(map(lambda trade: trade_helper.compute_profit(trade), trades))

    macd_strategy.execute(date, close)

    print(pprint.pformat(profit))


if __name__ == '__main__':
    main()
