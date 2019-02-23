from talib import MACD
import src.service.trade_helper as trade_helper
import src.service.strategy_helper_single_indicator as stragegy_helper_single_indicator


def execute(dates, price):
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)

    indicator = {
        'series': macdsignal,
        'rule': {
            'buy': 0,
            'sell': 0
        }
    }

    all_orders = stragegy_helper_single_indicator.get_orders(dates, price, indicator)
    all_orders_legacy_format = list(map(lambda x: (x['date'], x['operation'], x['price']), all_orders))
    statistics = trade_helper.compute_statistics_from_orders(all_orders_legacy_format)

    return trade_helper.compoe_lucros(statistics)
