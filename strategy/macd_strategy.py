from talib import MACD
import numpy as np

def execute(date, price):
    macd, macdsignal, macdhist = MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_dia_anterior = np.concatenate((np.array([np.nan]), macd[0:macd.shape[0]-1]))

    indicadores = np.array([[macd], [macd_dia_anterior]])

    print('ae')
