import numpy as np

import src.service.date_helper as date_helper
import src.service.file_io_service as file_io_service
import src.strategy.buy_and_hold_strategy as buy_and_hold_strategy
import src.strategy.macd_strategy as macd_strategy
import src.strategy.rsi_and_macd_strategy as rsi_and_macd_strategy
import src.strategy.rsi_strategy as rsi_strategy
import src.service.period_sampler_service as period_sampler_service
from pprint import pformat
import pandas as pd


def main():
    file_content = file_io_service.load_file('PETR4.SA')
    file_content = file_content.dropna()

    prices = file_content['Adj Close'].values
    dates = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    # dates, prices = period_sampler_service.do_single_sampling(dates, prices)

    all_stats = [
        buy_and_hold_strategy.execute(dates, prices),
        macd_strategy.execute(dates, prices),
        rsi_strategy.execute(dates, prices),
        rsi_and_macd_strategy.execute(dates, prices)
    ]

    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    # print(list(map(lambda x: x['name'] + ' ' + str(x['all_trades']['compount_profit']), all_stats)))
    names = np.array(list(map(lambda x: x['name'], all_stats)))
    compound_profit = np.array(list(map(lambda x: float(str(x['all_trades']['compount_profit'])), all_stats)))
    number_of_trades = np.array(list(map(lambda x: x['all_trades']['number_of_trades'], all_stats)))
    profit_mean = np.array(list(map(lambda x: float(str(x['all_trades']['profit']['mean'])), all_stats)))
    accuracies = np.array(list(map(lambda x: x['accuracy'], all_stats)))
    trade_period_mean = np.array(list(map(lambda x: x['all_trades']['period_of_trades']['mean'], all_stats)))

    df = pd.DataFrame({
        'name': names,
        'compound-profit': compound_profit,
        'number-of-trades': number_of_trades,
        'profit_mean': profit_mean,
        'accuracy': accuracies,
        'period_mean': trade_period_mean
    })

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

    # print(names)
    # print(compound_profit)
    # print(number_of_trades)
    # print(profit_mean)
    # print(accuracies)




if __name__ == '__main__':
    main()
