import math

import pandas as pd

from helpers import luby_sequence_df, episode_length, runtime#, compute_max_depth

if __name__ == '__main__':
    luby_df = luby_sequence_df(4000)
    l1 = 2
    l2 = 5
    depth = 10


    conjunction = True
    for depth in range(l1+1, 2000):
        eplength_1 = episode_length(luby_df, l1, depth, 1)
        eplength_2 = episode_length(luby_df, l2, depth, 1)

        if eplength_2 < eplength_1:
            runtime_1 = runtime(l1, depth, 1, luby_df)
            runtime_2 = runtime(l2, depth, 1, luby_df)
            conjunction = conjunction and (runtime_2 < runtime_1)

    print(conjunction)
