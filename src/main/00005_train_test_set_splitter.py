import src.service.file_io_service as file_io_service
import src.config.basic_config as basic_config


def do_split(company):
    file_content = file_io_service.load_file(company)
    file_content = file_content.dropna()
    index = int(len(file_content) * 80 / 100)


    return {
        'dev_set': file_content[0:index],
        'test_set': file_content[index:]
    }


def main():
    for company in basic_config.ativos:
        print(company)
        sets = do_split(company)
        sets['dev_set'].to_csv(r'/home/zem/labs/trading-project/data/dev/{}.csv'.format(company))
        sets['test_set'].to_csv(r'/home/zem/labs/trading-project/data/test/{}.csv'.format(company))

    print('oi')


if __name__ == '__main__':
    main()
