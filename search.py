import numpy as np


def hitting_time(series, probability_fn):
    """

    Parameters
    =============
    :param series, numpy.array:
    :param probability_fn, function: 

    Returns
    =============
    :return number, the hitting time for the series to halt on the given probability function
    """

    acc = 0
    for episode in series:
        for i in range(1, episode + 1):
            if halt(probability_fn, i):
                # halt algorithm
                return acc + i
        acc += episode

    # Never found a goal after completing the entire series
    #raise exceptions.SequenceTooShortException(series, 'Did not halt')
    print("No Halt")
    return np.nan



def halt(probability_fn, depth):
    """
    """
    return np.random.uniform() < probability_fn(depth)
