import src.service.trade_helper as trade_helper


def nao_estou_comprado_logic(indicator, i):
    return 'COMPRAR' if indicator['series'][i] > indicator['rule']['buy'] else 'NOP'


def estou_comprado_logic(indicator, i):
    return 'VENDER' if indicator['series'][i] < indicator['rule']['sell'] else 'NOP'


def create_operation_for_today(dates, estou_comprado, indicator, i):
    operation = estou_comprado_logic(indicator, i) if estou_comprado else nao_estou_comprado_logic(indicator, i)

    return dates[i], operation


def get_orders(dates, price, indicator):
    estou_comprado = False

    all_operations = []
    for i in range(0, len(dates)):
        date, operation = create_operation_for_today(dates, estou_comprado, indicator, i)
        estou_comprado = trade_helper.resolve_estou_comprado_flag(estou_comprado, operation)
        all_operations.append((date, operation, price[i]))

    filtered = list(filter(lambda x: x[1] != 'NOP', all_operations))

    if len(filtered) > 0 and filtered[-1][1] == 'COMPRAR':
        filtered.append((dates[-1], 'VENDER', price[-1]))

    return filtered
