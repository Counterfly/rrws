import functools
import math
import multiprocessing

import pandas as pd
import numpy as np

import helpers
#from helpers import luby_sequence_df, episode_length, runtime#, compute_max_depth
import luby_helper
import search



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
    """
    TODO:
      replace input_depth with episode_index, input_depth (have the series be fixed arguments via functools)
    """
    if input_depth == p_depth:
        return p_value
    return 0

def worker(probability_fn, series):
    return search.hitting_time(series, probability_fn)

if __name__ == '__main__':
    luby_df = helpers.luby_sequence_df(20000)
    luby_df = pd.Series(luby_df['luby'])
    print(luby_df[:10])
    print('-' * 20)
    print("max value is", luby_df.max())
    l1 = 2
    l2 = 3


    NUM_ITERATIONS = 1000
    df = pd.DataFrame()
    min_depth = l1
    while min_depth < 129:
        # Favourable depth for l1 relative to l2
        fav_depth = helpers.find_favourable_runtime_depth(
               l1 * luby_df,
               l2 * luby_df,
               min_depth=min_depth
        )
        print("Fav depth =", fav_depth)

        '''
        Pickle can't serialize a closure function so the workaround
        is to use functools.partial to essentially bind the first
        variables to the function call and wait for the remaining ones
        to invoke the function "full"-y
        '''
        #probability_fn = probability_single_depth(fav_depth, 0.01)
        p_fn = functools.partial(probability_fn, 0.01, fav_depth)
        func = functools.partial(worker, p_fn)

        pool = multiprocessing.Pool(2)
        hitting_times1 = pool.map(func, [l1 * luby_df] * NUM_ITERATIONS)
        hitting_times2 = pool.map(func, [l2 * luby_df] * NUM_ITERATIONS)

        pool.close() # no more tasks
        pool.join()  # wrap up current tasks

        df_dict = {
            'depth': fav_depth,
            'num_iterations': NUM_ITERATIONS,
            'l1': np.asarray(hitting_times1).mean(),
            'l2': np.asarray(hitting_times2).mean()
        }
        df = df.append(df_dict, ignore_index=True)
        min_depth = fav_depth + 1

    df.to_csv('./df.csv')
    print(df)
