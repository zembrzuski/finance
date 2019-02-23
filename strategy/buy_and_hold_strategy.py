import service.trade_helper as trade_helper


def get_orders(dates, price):
    all_operations = []

    all_operations.append((dates[0], 'COMPRAR', price[0]))
    all_operations.append((dates[-1], 'VENDER', price[-1]))

    return all_operations


def execute(dates, price):
    all_orders = get_orders(dates, price)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)
    return trade_helper.compoe_lucros(statistics)
