import numpy as np

def compute_profit(a_trade):
    return {
        'trade_time': a_trade['sell']['date'] - a_trade['buy']['date'],
        'profit_percentage': (a_trade['sell']['value'] / a_trade['buy']['value'] - 1) * 100
    }


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


def compoe_lucros(statistics):
    lucros = np.array(list(map(lambda x: x['percentual_lucro'], statistics)))

    dinheiro = 100

    for lucro in lucros:
        dinheiro = (lucro / 100 * dinheiro) + dinheiro

    return dinheiro - 100


def resolve_estou_comprado_flag(estou_comprado, operation):
    if operation == 'COMPRAR':
        return True
    elif operation == 'VENDER':
        return False
    else:
        return estou_comprado
