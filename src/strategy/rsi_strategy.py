from talib import RSI
import src.service.trade_helper as trade_helper


def estou_comprado_logic(rsi, i):
    return 'VENDER' if rsi[i] > 75 else 'NOP'


def nao_estou_comprado_logic(rsi, i):
    return 'COMPRAR' if rsi[i] < 25 else 'NOP'


def create_operation_for_today(rsi, date, estou_comprado, i):
    operation = estou_comprado_logic(rsi, i) if estou_comprado else nao_estou_comprado_logic(rsi, i)
    return date[i], operation


def get_orders(rsi, dates, price):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(rsi)):
        date, operation = create_operation_for_today(rsi, dates, estou_comprado, i)
        estou_comprado = trade_helper.resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append((date, operation, price[i]))

    filtered = list(filter(lambda x: x[1] != 'NOP', all_operations))

    if len(filtered) > 0 and filtered[-1][1] == 'COMPRAR':
        filtered.append((dates[-1], 'VENDER', price[-1]))

    return filtered


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)
    all_orders = get_orders(rsi, dates, price)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    return trade_helper.compoe_lucros(statistics)
