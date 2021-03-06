from talib import RSI
import src.service.trade_helper as trade_helper
import src.service.strategy_helper_single_indicator as stragegy_helper_single_indicator
import copy


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)

    indicator = {
        'series': rsi,
        'go_up': rsi < 25,
        'go_down': rsi > 75
    }

    all_orders = stragegy_helper_single_indicator.get_orders(dates, price, indicator)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    new_stats = copy.deepcopy(statistics)
    new_stats['name'] = 'rsi'

    return new_stats
