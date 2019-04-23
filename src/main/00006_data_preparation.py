import src.service.file_io_service as file_io_service
import random
import numpy as np


def main():
    company_code = 'PETR4.SA'

    dates, prices = file_io_service.get_historical_data(company_code)

    my_dataframe = np.transpose(np.concatenate(([dates], [prices]), axis=0))

    # just for test
    my_dataframe = my_dataframe[[0, 1, 2, 3, 4], :]

    tomorrow_prices = np.transpose([np.append(my_dataframe[:, 1][1:], 0)])

    vai = np.hstack((my_dataframe, tomorrow_prices))

    print(vai)
    print('finished')


if __name__ == '__main__':
    main()
