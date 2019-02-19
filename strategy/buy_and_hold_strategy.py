import numpy as np


def execute(date, close):
    trade = {
        'buy': {
            'date': date[0],
            'value': close[0]
        },
        'sell': {
            'date': date[-1],
            'value': close[-1]
        }
    }

    return np.array([trade])
