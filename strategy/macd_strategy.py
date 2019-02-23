from talib import MACD
import service.trade_helper as trade_helper


def nao_estou_comprado_logic(macdsignal, i):
    return 'COMPRAR' if macdsignal[i] > 0 else 'NOP'


def estou_comprado_logic(macdsignal, i):
    return 'VENDER' if macdsignal[i] < 0 else 'NOP'


def create_operation_for_today(macdsignal, date, estou_comprado, i):
    operation = estou_comprado_logic(macdsignal, i) if estou_comprado else nao_estou_comprado_logic(macdsignal, i)
    return date[i], operation


def get_orders(macdsignal, dates, price):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(macdsignal)):
        date, operation = create_operation_for_today(macdsignal, dates, estou_comprado, i)
        estou_comprado = trade_helper.resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append((date, operation, price[i]))

    filtered = list(filter(lambda x: x[1] != 'NOP', all_operations))

    if filtered[-1][1] == 'COMPRAR':
        filtered.append((dates[-1], 'VENDER', price[-1]))

    return filtered


def execute(dates, price):
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    all_orders = get_orders(macdsignal, dates, price)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)
    return trade_helper.compoe_lucros(statistics)
