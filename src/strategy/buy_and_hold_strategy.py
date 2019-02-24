import src.service.trade_helper as trade_helper
from decimal import *
import numpy as np


def get_orders(dates, price):
    all_operations = []

    all_operations.append({
        'date': dates[0],
        'operation': 'COMPRAR',
        'price': Decimal(price[0]),
        'indicator': np.nan
    })

    all_operations.append({
        'date': dates[-1],
        'operation': 'VENDER',
        'price': Decimal(price[-1]),
        'indicator': np.nan
    })

    return all_operations


def execute(dates, price):
    all_orders = get_orders(dates, price)
    statistics = trade_helper.compute_statistics_from_orders(all_orders)

    return statistics

