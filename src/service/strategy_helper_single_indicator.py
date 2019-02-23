import src.service.trade_helper as trade_helper
from decimal import *


def have_not_bought_logic(indicator, i):
    return 'COMPRAR' if indicator['series'][i] > indicator['rule']['buy'] else 'NOP'


def have_bought_logic(indicator, i):
    return 'VENDER' if indicator['series'][i] < indicator['rule']['sell'] else 'NOP'


def create_operation_for_today(dates, estou_comprado, indicator, i):
    operation = have_bought_logic(indicator, i) if estou_comprado else have_not_bought_logic(indicator, i)

    return {
        'date': dates[i],
        'operation': operation,
        'indicator_value': indicator['series'][i]
    }


def get_orders(dates, price, indicator):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(dates)):
        operation_data = create_operation_for_today(dates, estou_comprado, indicator, i)
        operation = operation_data['operation']
        estou_comprado = trade_helper.resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append({
            'date': operation_data['date'],
            'operation': operation,
            'price': Decimal(price[i]),
            'indicator': indicator['series'][i]
        })

    filtered = list(filter(lambda x: x['operation'] != 'NOP', all_operations))

    if len(filtered) > 0 and filtered[-1]['operation'] == 'COMPRAR':
        filtered.append({
            'date': dates[-1],
            'operation': 'VENDER',
            'price': Decimal(price[-1]),
            'indicator': indicator['series'][-1]
        })

    return filtered
