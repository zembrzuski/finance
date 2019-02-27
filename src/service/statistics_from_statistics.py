import numpy as np

def compute_statistics_from_statistics_for_a_strategy(statistics):
    new_dict = dict()

    for k, v in statistics.items():
        new_dict[k] = np.mean(v)

    return new_dict


def compute_statistics_from_statistics_for_all_strategies(all_iterations_statistics):
    new_dict = dict()

    for k, v in all_iterations_statistics.items():
        new_dict[k] = compute_statistics_from_statistics_for_a_strategy(v)

    return new_dict
