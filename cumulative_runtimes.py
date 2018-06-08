import math

import pandas as pd

from helpers import luby_sequence_df, episode_length, runtime#, compute_max_depth

if __name__ == '__main__':
    luby_df = luby_sequence_df(4000)
    l1 = 2
    l2 = 5
    depth = 10

    print(episode_length(luby_df, l1, depth, 1))
    print(episode_length(luby_df, l2, depth, 1))
    print(runtime(l1, depth, 1, luby_df), "vs", runtime(l2, depth, 1, luby_df))
    print(runtime(l1, depth, 15, luby_df), "vs", runtime(l2, depth, 15, luby_df))

    #max_depth = compute_max_depth(l1, l2)
    #print("max depth is", max_depth)
    for depth in range(l1+1, 500):
        runtime_oscilates = False
        length1 = episode_length(luby_df, l1, depth, 1)
        length2 = episode_length(luby_df, l2, depth, 1)

        runtime1 = runtime(l1, depth, 1, luby_df)
        runtime2 = runtime(l2, depth, 1, luby_df)
        #if runtime2 <= runtime1:
        if runtime2 <= runtime1:
            for n_times in range(3,50):
                runtime1a = runtime(l1, depth, n_times, luby_df)
                runtime2a = runtime(l2, depth, n_times, luby_df)
                if runtime1a < runtime2a:
                    runtime_oscilates = True
                    break
            #if length2 >= length1:
            #    print("L2 >= L1", depth, length1, length2, "rt=", runtime1, "vs", runtime2)
            if length1 >= length2:
                print("L1 >= L2", depth, length1, length2, "rt=", runtime1, "vs", runtime2)
        #print("Finished depth", depth, ", oscilates = ", runtime_oscilates)
