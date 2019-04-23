import numpy as np

import src.service.date_helper as date_helper
import src.service.file_io_service as file_io_service
import src.strategy.buy_and_hold_strategy as buy_and_hold_strategy
import src.strategy.macd_strategy as macd_strategy
import src.strategy.rsi_and_macd_strategy as rsi_and_macd_strategy
import src.strategy.rsi_strategy as rsi_strategy
import src.service.period_sampler_service as period_sampler_service
import src.service.statistics_from_statistics as statistics_from_statistics
from pprint import pformat

def extract_simple_information(statistics, strategy_key, all_iterations_statistics):
    strategy_statistics = all_iterations_statistics.get(strategy_key)

    return {
        'compount_profit': np.append(strategy_statistics['compount_profit'], statistics['all_trades']['compount_profit']),
        'number_of_trades': np.append(strategy_statistics['number_of_trades'], statistics['all_trades']['number_of_trades']),
        'profit_mean': np.append(strategy_statistics['profit_mean'], statistics['all_trades']['profit']['mean']),
        'accuracy': np.append(strategy_statistics['accuracy'], statistics['accuracy']),
        'period_of_trades_mean': np.append(strategy_statistics['period_of_trades_mean'], statistics['all_trades']['period_of_trades']['mean'])
    }


def create_statistics_strategy():
    return {
        'compount_profit': np.array([]),
        'number_of_trades': np.array([]),
        'profit_mean': np.array([]),
        'accuracy': np.array([]),
        'period_of_trades_mean': np.array([])
    }


def iterate(dates_inp, prices_inp, iterations):
    all_iterations_statistics = {
        'buy-and-hold': create_statistics_strategy(),
        'macd': create_statistics_strategy(),
        'rsi': create_statistics_strategy(),
        'rsi-and-macd': create_statistics_strategy()
    }

    for i in range(0, iterations):
        # dates, prices = period_sampler_service.sample_a_random_year(dates_inp, prices_inp)
        dates, prices = period_sampler_service.do_single_sampling(dates_inp, prices_inp)

        all_iterations_statistics['buy-and-hold'] = extract_simple_information(
            buy_and_hold_strategy.execute(dates, prices), 'buy-and-hold', all_iterations_statistics)

        all_iterations_statistics['macd'] = extract_simple_information(
            macd_strategy.execute(dates, prices), 'macd', all_iterations_statistics)

        all_iterations_statistics['rsi'] = extract_simple_information(
            rsi_strategy.execute(dates, prices), 'rsi', all_iterations_statistics)

        all_iterations_statistics['rsi-and-macd'] = extract_simple_information(
            rsi_and_macd_strategy.execute(dates, prices), 'rsi-and-macd', all_iterations_statistics)

    return all_iterations_statistics


def main():
    # np.random.seed(0)
    file_content = file_io_service.load_historical_data('PETR4.SA')
    file_content = file_content.dropna()

    prices = file_content['Adj Close'].values
    dates = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date'])))

    # dates, prices = period_sampler_service.do_single_sampling(dates, prices)
    all_iterations_statistics = iterate(dates, prices, 1000)

    summary = statistics_from_statistics.compute_statistics_from_statistics_for_all_strategies(all_iterations_statistics)

    print(pformat(summary))
    print('oi')


if __name__ == '__main__':
    main()
