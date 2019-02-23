from talib import RSI
import src.service.trade_helper as trade_helper
import src.service.strategy_helper_single_indicator as stragegy_helper_single_indicator


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)

    indicator = {
        'series': rsi,
        'go_up': rsi < 25,
        'go_down': rsi > 75
    }

    all_orders = stragegy_helper_single_indicator.get_orders(dates, price, indicator)
    all_orders_legacy_format = list(map(lambda x: (x['date'], x['operation'], x['price']), all_orders))
    statistics = trade_helper.compute_statistics_from_orders(all_orders_legacy_format)

    return trade_helper.compoe_lucros(statistics)
