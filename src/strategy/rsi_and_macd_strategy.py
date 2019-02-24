from talib import RSI, MACD
import src.service.trade_helper as trade_helper
import src.service.strategy_helper_single_indicator as stragegy_helper_single_indicator
import copy


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)

    rsi_buy = (rsi < 30) + 0
    rsi_sell = (rsi > 70) + 0

    macd_buy = (macdsignal > 0) + 0
    macd_sell = (macdsignal < 0) + 0

    indicator = {
        'series': macdsignal,
        'go_up': (rsi_buy + macd_buy) == 2,
        'go_down': (rsi_sell + macd_sell) == 2
    }

    all_orders = stragegy_helper_single_indicator.get_orders(dates, price, indicator)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    new_stats = copy.deepcopy(statistics)
    new_stats['name'] = 'rsi+macd'

    return new_stats
