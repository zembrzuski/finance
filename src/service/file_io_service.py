import os
import pandas
import src.config.basic_config as basic_config


def persist_file(company_code, csv_content):
    f = open('{}{}.csv'.format(basic_config.data_local_storage_filepath, company_code), "w+")
    f.write(csv_content)
    f.close()

    return True


def load_file(company_code):
    return pandas.read_csv('{}{}.csv'.format(basic_config.data_local_storage_filepath, company_code).format(company_code))


def persist_on_disk_a_company(company):
    file_path = '{}/{}.csv'.format(basic_config.data_local_storage_filepath, company['company_code'])

    if os.path.isfile(file_path):
        os.remove(file_path)

    f = open(file_path, "w+")
    f.write(company['historical_data'])
    f.close()

    return company['company_code'], True
