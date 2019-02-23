from talib import RSI, MACD
import numpy as np
import service.trade_helper as trade_helper


def estou_comprado_logic(rsi, macdsignal, i):
    return 'VENDER' if rsi[i] > 70 and macdsignal[i] < 0 else 'NOP'


def nao_estou_comprado_logic(rsi, macdsignal, i):
    return 'COMPRAR' if rsi[i] < 30 and macdsignal[i] > 0else 'NOP'


def create_operation_for_today(rsi, macdsignal, date, estou_comprado, i):
    operation = estou_comprado_logic(rsi, macdsignal, i) \
        if estou_comprado \
        else nao_estou_comprado_logic(rsi, macdsignal, i)

    return date[i], operation


def get_orders(rsi, macdsignal, dates, price):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(rsi)):
        date, operation = create_operation_for_today(rsi, macdsignal, dates, estou_comprado, i)
        estou_comprado = trade_helper.resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append((date, operation, price[i]))

    filtered = list(filter(lambda x: x[1] != 'NOP', all_operations))

    if filtered[-1][1] == 'COMPRAR':
        filtered.append((dates[-1], 'VENDER', price[-1]))

    return filtered


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    all_orders = get_orders(rsi, macdsignal, dates, price)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    return trade_helper.compoe_lucros(statistics)
