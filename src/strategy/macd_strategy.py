from talib import MACD
import src.service.trade_helper as trade_helper
import src.service.strategy_helper_single_indicator as stragegy_helper_single_indicator


def execute(dates, price):
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)

    indicator = {
        'series': macdsignal,
        'go_up': macdsignal > 0,
        'go_down': macdsignal < 0
    }

    all_orders = stragegy_helper_single_indicator.get_orders(dates, price, indicator)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    return statistics['all_trades']['compount_profit'].real
