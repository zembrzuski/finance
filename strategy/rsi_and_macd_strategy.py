from talib import RSI, MACD
import numpy as np


def estou_comprado_logic(rsi, macdsignal, i):
    return 'VENDER' if rsi[i] > 70 and macdsignal[i] < 0 else 'NOP'


def nao_estou_comprado_logic(rsi, macdsignal, i):
    return 'COMPRAR' if rsi[i] < 30 and macdsignal[i] > 0else 'NOP'


def resolve_estou_comprado_flag(estou_comprado, operation):
    if operation == 'COMPRAR':
        return True
    elif operation == 'VENDER':
        return False
    else:
        return estou_comprado


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
        estou_comprado = resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append((date, operation, price[i]))

    filtered = list(filter(lambda x: x[1] != 'NOP', all_operations))

    if filtered[-1][1] == 'COMPRAR':
        filtered.append((dates[-1], 'VENDER', price[-1]))

    return filtered



def compute_statistics_from_orders(all_orders):
    statistics = []

    for i in range(0, len(all_orders), 2):
        ordem_compra = all_orders[i]
        ordem_venda = all_orders[i+1]

        numero_dias_ordem = ordem_venda[0] - ordem_compra[0]
        percentual_lucro = ((ordem_venda[2] / ordem_compra[2])-1)*100

        statistics.append({
            'numero_dias_ordem': numero_dias_ordem,
            'percentual_lucro': percentual_lucro
        })

    return statistics


def execute(dates, price):
    rsi = RSI(price, timeperiod=14)
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    all_orders = get_orders(rsi, macdsignal, dates, price)
    statistics = compute_statistics_from_orders(all_orders)

    lucros = np.array(list(map(lambda x: x['percentual_lucro'], statistics)))

    # print('\n'.join(list(map(lambda x: str(x[0]) + ' ' + x[1] + '\t' + str(x[2]), all_orders))))
    nplucros = np.array(lucros)

    return np.sum(nplucros)
