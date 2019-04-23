import src.service.file_io_service as file_io_service


def main():
    company_code = 'PETR4.SA'

    dates, prices = file_io_service.get_historical_data(company_code)

    print('oi')


if __name__ == '__main__':
    main()
