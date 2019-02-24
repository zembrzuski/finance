import numpy as np
from decimal import *

def decimal_from_float(inpt):
    return decimal_from_decimal(Decimal(inpt))

def decimal_from_decimal(inpt):
    return inpt.quantize(Decimal('.000001'), rounding=ROUND_DOWN)

def create_single_trade_statistics(ordem_compra, ordem_venda):
    numero_dias_ordem = ordem_venda['date'] - ordem_compra['date']
    percentual_lucro = ((ordem_venda['price'] / ordem_compra['price']) - Decimal(1)) * Decimal(100)

    return {
        'numero_dias_ordem': numero_dias_ordem.days,
        'percentual_lucro': percentual_lucro,
        'buy_indicator': ordem_compra['indicator'],
        'sell_indicator': ordem_venda['indicator']
    }


def create_multiple_trades_statistics(trade_statistics_list):
    all_buy_indicators = np.array(list(map(lambda x: x['buy_indicator'], trade_statistics_list)))
    all_sell_indicators = np.array(list(map(lambda x: x['sell_indicator'], trade_statistics_list)))
    all_periods = np.array(list(map(lambda x: x['numero_dias_ordem'], trade_statistics_list)))
    all_profits = np.array(list(map(lambda x: x['percentual_lucro'], trade_statistics_list)))

    return {
        'compount_profit': decimal_from_decimal(compoe_lucros(trade_statistics_list)),
        'number_of_trades': len(trade_statistics_list),
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
            'mean': decimal_from_decimal(np.mean(all_profits)),
            'sd_dev': decimal_from_decimal(np.std(all_profits))
        }
    }


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
    success_trades_statistics = []
    failed_trades_statistics = []

    for i in range(0, len(all_orders), 2):
        current_trade_statistics = create_single_trade_statistics(all_orders[i], all_orders[i+1])
        trades_statistics.append(current_trade_statistics)

        if current_trade_statistics['percentual_lucro'] > 0:
            success_trades_statistics.append(current_trade_statistics)
        else:
            failed_trades_statistics.append(current_trade_statistics)


    return {
        'all_trades': create_multiple_trades_statistics(trades_statistics),
        'success_trades': create_multiple_trades_statistics(success_trades_statistics),
        'failed_trades': create_multiple_trades_statistics(failed_trades_statistics)
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
