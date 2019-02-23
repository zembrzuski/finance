import numpy as np


def do_single_sampling(dates, prices):
    low = int(np.random.uniform(0, len(dates)))
    high = int(np.random.uniform(low, len(dates)))

    return dates[low:high], prices[low:high]
