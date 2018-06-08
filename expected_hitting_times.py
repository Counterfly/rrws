import functools
import math
import multiprocessing

import pandas as pd

import helpers
#from helpers import luby_sequence_df, episode_length, runtime#, compute_max_depth
import luby_helper



def probability_single_depth(depth, p_value):
    """


    Parameters:
    =============
    :param depth
    :param p_value

    Returns
    =============
    :return probability_function, function that given an input depth returns the probability of escaping/finding goal.
    """
    def _helper(input_depth):
        if input_depth == depth:
            return p_value
        return 0
    return _helper


def probability_fn(p_value, p_depth, input_depth):
    if input_depth == p_depth:
        return p_value
    return 0

def worker(probability_fn, series):
    return 1
    #return helpers.hitting_time(series, probability_fn)

if __name__ == '__main__':
    luby_df = helpers.luby_sequence_df(4000)
    luby_df = pd.Series(luby_df['luby'])
    print(luby_df[:10])
    print('-' * 20)
    print("max value is", luby_df.max())
    l1 = 2
    l2 = 3

    # Favourable depth for l1 relative to l2
    fav_depth = helpers.find_favourable_runtime_depth(
           l1 * luby_df,
           l2 * luby_df,
           min_depth=50
    )
    print("Fav depth =", fav_depth)
    #probability_fn = probability_single_depth(fav_depth, 0.01)

    p_fn = functools.partial(probability_fn, 0.01, fav_depth)
    NUM_ITERATIONS = 10
    pool = multiprocessing.Pool(4)

    func = functools.partial(worker, p_fn)
    hitting_times1 = pool.map(func, [l1 * luby_df] * NUM_ITERATIONS)
    hitting_times2 = pool.map(func, [l2 * luby_df] * NUM_ITERATIONS)

    pool.close() # no more tasks
    pool.join()  # wrap up current tasks

    print(pd.DataFrame({'l1': hitting_times1, 'l2': hitting_times2}))
