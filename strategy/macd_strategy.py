from talib import MACD
import numpy as np


def nao_estou_comprado_logic(macdsignal, i):
    return 'COMPRAR' if macdsignal[i] > 0 else 'NOP'


def estou_comprado_logic(macdsignal, i):
    return 'VENDER' if macdsignal[i] < 0 else 'NOP'


def create_operation_for_today(macdsignal, date, estou_comprado, i):
    operation = estou_comprado_logic(macdsignal, i) if estou_comprado else nao_estou_comprado_logic(macdsignal, i)
    return date[i], operation


def resolve_estou_comprado_flag(estou_comprado, operation):
    if operation == 'COMPRAR':
        return True
    elif operation == 'VENDER':
        return False
    else:
        return estou_comprado


def get_orders(macdsignal, dates, price):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(macdsignal)):
        date, operation = create_operation_for_today(macdsignal, dates, estou_comprado, i)
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



def compoe_lucros(lucros):
    dinheiro = 100

    for lucro in lucros:
        dinheiro = (lucro / 100 * dinheiro) + dinheiro

    return dinheiro - 100



def execute(dates, price):
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    all_orders = get_orders(macdsignal, dates, price)

    statistics = compute_statistics_from_orders(all_orders)

    lucros = np.array(list(map(lambda x: x['percentual_lucro'], statistics)))

    # print('\n'.join(list(map(lambda x: str(x[0]) + ' ' + x[1] + '\t' + str(x[2]), all_orders))))
    nplucros = compoe_lucros(lucros)

    return np.sum(nplucros)


