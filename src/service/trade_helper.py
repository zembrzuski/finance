import numpy as np
from decimal import *


def compute_profit(a_trade):
    return {
        'trade_time': a_trade['sell']['date'] - a_trade['buy']['date'],
        'profit_percentage': (a_trade['sell']['value'] / a_trade['buy']['value'] - 1) * 100
    }


def compute_statistics_from_orders(all_orders):
    # all_orders eh uma lista de order
    # order eh uma tupla como no exemplo: (datetime, 'COMPRAR', Decimal(34.35))
    # order eh uma tupla como no exemplo: (datetime, 'NOP', Decimal(3.35))
    # order eh uma tupla como no exemplo: (datetime, 'VENDER', Decimal(1.2))

    statistics = []

    for i in range(0, len(all_orders), 2):
        ordem_compra = all_orders[i]
        ordem_venda = all_orders[i+1]

        numero_dias_ordem = ordem_venda[0] - ordem_compra[0]
        percentual_lucro = ((Decimal(ordem_venda[2]) / Decimal(ordem_compra[2]))-Decimal(1))*Decimal(100)

        statistics.append({
            'numero_dias_ordem': numero_dias_ordem,
            'percentual_lucro': percentual_lucro
        })

    return statistics


def compoe_lucros(statistics):
    # statistics eh um dict como no exempo
    # {
    #   'numero_dias_ordem': DIFERENCA ENTRE DOIS DATETIMES (nao lembro qual eh o tipo do objeto)
    #   'percentual_lucro': Decimal(32.5)  --> isso no caso do trade ter dado 32.5% de lucro.
    # }

    lucros = np.array(list(map(lambda x: x['percentual_lucro'], statistics)))

    dinheiro = Decimal(100.)

    for lucro in lucros:
        dinheiro = (lucro / Decimal(100.) * dinheiro) + dinheiro

    return dinheiro - Decimal(100.)


def resolve_estou_comprado_flag(estou_comprado, operation):
    if operation == 'COMPRAR':
        return True
    elif operation == 'VENDER':
        return False
    else:
        return estou_comprado
