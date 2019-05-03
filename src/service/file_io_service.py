import os
import pandas
import src.config.basic_config as basic_config
import src.service.date_helper as date_helper
import numpy as np


def persist_file(company_code, csv_content):
    f = open('{}{}.csv'.format(basic_config.data_local_storage_filepath, company_code), "w+")
    f.write(csv_content)
    f.close()

    return True


def load_historical_data(company_code):
    return pandas.read_csv('{}{}.csv'.format(basic_config.data_local_storage_filepath, company_code).format(company_code))


def persist_on_disk_a_company(company):
    file_path = '{}/{}.csv'.format(basic_config.data_local_storage_filepath, company['company_code'])

    if os.path.isfile(file_path):
        os.remove(file_path)

    f = open(file_path, "w+")
    f.write(company['historical_data'])
    f.close()

    return company['company_code'], True


def get_historical_data(company_code):
    historical_data = load_historical_data(company_code)
    historical_data = historical_data.dropna()

    prices = historical_data['Adj Close'].values
    dates = np.array(list(map(lambda x: date_helper.parse_date_to_datetime(x), historical_data['Date'])))
    volume = historical_data['Volume'].values

    return dates, prices, volume


def read_csv(company_code):
    historical_data = load_historical_data(company_code)
    historical_data = historical_data.dropna()
    historical_data = historical_data.reset_index(drop=True)

    return historical_data
