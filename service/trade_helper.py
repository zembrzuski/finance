

def compute_profit(a_trade):
    return {
        'trade_time': a_trade['sell']['date'] - a_trade['buy']['date'],
        'profit_percentage': (a_trade['sell']['value'] / a_trade['buy']['value'] - 1) * 100
    }
