import numpy as np
from talib import RSI, MACD, BBANDS
import src.service.file_io_service as file_io_service
import src.service.date_helper as date_helper
import pandas as pd


def get_labeled_quotes(company_code):
    historical_data = file_io_service.read_csv(company_code)

    dates = np.array(list(map(lambda x: pd.Timestamp(x, tz=None), historical_data['Date'])))

    historical_data = historical_data.assign(Datee=pd.Series(dates))

    next_day_close = np.array(historical_data['Close'][1:])
    next_day_close = np.append(next_day_close, -1)

    historical_data = historical_data.assign(Next_Day_Close=pd.Series(next_day_close))
    historical_data = historical_data.drop([historical_data.shape[0]-1])

    return historical_data


def main():
    print('init data preparation')
    company_code = 'PETR4.SA'

    historical_data = get_labeled_quotes(company_code)

    print('finished')


if __name__ == '__main__':
    main()
