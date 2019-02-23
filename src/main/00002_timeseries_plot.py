import src.service.file_io_service as file_io_service
import src.service.date_helper as date_helper
import matplotlib.pyplot as plt


def main():
    file_content = file_io_service.load_file('PETR4.SA')

    value = file_content['Adj Close'].values
    date = list(map(lambda x: date_helper.parse_date_to_datetime(x), file_content['Date']))

    plt.plot(date, value)
    plt.show()


if __name__ == '__main__':
    main()
