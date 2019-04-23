import src.service.file_io_service as file_io_service
import random
import numpy as np


def slice_remover(data, init_index, finish_index):
    data_first_part = data[0:init_index]
    data_second_part = data[finish_index:len(data)]

    return np.concatenate((data_first_part, data_second_part), axis=0)


def extract_period_for_testset(dates, prices, period_length):
    init_index = random.randint(0, len(dates)-period_length)
    finish_index = init_index + period_length

    return {
        'dev': {
            'dates': slice_remover(dates, init_index, finish_index),
            'prices': slice_remover(prices, init_index, finish_index)
        },
        'test': {
            'dates': dates[init_index:finish_index],
            'prices': prices[init_index:finish_index]
        },
        'indexes': {
            'init': init_index,
            'finish': finish_index
        }
    }


def rebuild_original_set_with_dev_and_test(splitted_structure):
    init_index = splitted_structure['indexes']['init']

    return np.concatenate((
        splitted_structure['dev']['dates'][0:init_index],
        splitted_structure['test']['dates'],
        splitted_structure['dev']['dates'][init_index:len(splitted_structure['dev']['dates'])]
    ), axis=0)


def main():
    company_code = 'PETR4.SA'

    dates, prices = file_io_service.get_historical_data(company_code)

    split = extract_period_for_testset(dates, prices, 200)
    rebuilt = rebuild_original_set_with_dev_and_test(split)

    # TODO o que fazer agora??
    # fazer 2 splits por empresa.
    # persistir os bagulho splitado
    # depois, fazer machine learning com o dev+test sets
    
    print(np.alltrue(dates == rebuilt))


if __name__ == '__main__':
    main()
