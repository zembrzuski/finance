import numpy as np
from decimal import *


def compute_statistics_from_orders(all_orders):
    """
    all_orders eh uma lista de order
    order eh uma dict conforme abaixo
    {
        'date': datetime,
        'operation': 'COMPRAR' ou 'VENDER',
        'price': Decimal(price[i]),
        'indicator': indicator['series'][i]
    }
    """

    trades_statistics = []

    for i in range(0, len(all_orders), 2):
        ordem_compra = all_orders[i]
        ordem_venda = all_orders[i+1]

        numero_dias_ordem = ordem_venda['date'] - ordem_compra['date']
        percentual_lucro  = ((ordem_venda['price'] / ordem_compra['price']) - Decimal(1)) * Decimal(100)

        trades_statistics.append({
            'numero_dias_ordem': numero_dias_ordem.days,
            'percentual_lucro': percentual_lucro,
            'buy_indicator': ordem_compra['indicator'],
            'sell_indicator': ordem_venda['indicator']
        })

    all_buy_indicators = np.array(list(map(lambda x: x['buy_indicator'], trades_statistics)))
    all_sell_indicators = np.array(list(map(lambda x: x['sell_indicator'], trades_statistics)))
    all_periods = np.array(list(map(lambda x: x['numero_dias_ordem'], trades_statistics)))
    all_profits = np.array(list(map(lambda x: x['percentual_lucro'], trades_statistics)))

    return {
        'all_trades': {
            'compount_profit': compoe_lucros(trades_statistics),
            'number_of_trades': len(trades_statistics),
            'buy_indicator': {
                'mean': np.mean(all_buy_indicators),
                'sd_dev': np.std(all_buy_indicators)
            },
            'sell_indicator': {
                'mean': np.mean(all_sell_indicators),
                'sd_dev': np.std(all_sell_indicators)
            },
            'period_of_trades': {
                'mean': np.mean(all_periods),
                'sd_dev': np.std(all_periods)
            },
            'profit': {
                'mean': np.mean(all_profits),
                'sd_dev': np.std(all_profits)
            }
        }
    }


def compoe_lucros(statistics):
    """
    statistics eh um dict como no exempo
    {
      'numero_dias_ordem': DIFERENCA ENTRE DOIS DATETIMES (nao lembro qual eh o tipo do objeto)
      'percentual_lucro': Decimal(32.5)  --> isso no caso do trade ter dado 32.5% de lucro.
    }
    """

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
