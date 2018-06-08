import math

# 3rd party modules
import pandas as pd


# User modules
import exceptions


def episode_length(sequence_df, scalar, depth, nth_time):
    """
    Gets the episode length to reach depth `depth` for the `nth_time` using the sequence defined in `sequence_df`
    which is subsequently scaled by `scalar`.
    L(scalar*sequence_df, depth, nth_time)

    Parameters
    =============
    :param

    Returns
    =============
    :return the length of the episode 
    """
    column_name = list(sequence_df)[0]
    sequence_minimum = math.ceil(depth/float(scalar))
    df = sequence_df[sequence_df[column_name] >= sequence_minimum]

    assert len(df) >= nth_time, "Need to increase length of sequence"
    df = df.iloc[nth_time-1] * scalar
    return df.values[0]


def hitting_time_index(sequence_df, scalar, depth, nth_time):
    """
    Gets the index of the sequence value that reaches depth `depth` for the `nth_time` in the sequence defined in `sequence_df` and which is subsequently scaled by `scalar`.
    Therefore, you can retrieve the episode length by: sequence_df.iloc[hitting_time_index(...)]

    Return
    =============
    :return 
    """
    column_name = list(sequence_df)[0]
    sequence_minimum = math.ceil(depth/float(scalar))
    df = sequence_df[sequence_df[column_name] >= sequence_minimum]

    assert len(df) >= nth_time, "Need to increase length of sequence"
    df = df[:nth_time] * scalar

    # Get index of last row
    last_index = df.index.values[-1]
    return last_index


def runtime(scalar, depth, nth_time, sequence_df):
    # Get index of last row
    last_index = hitting_time_index(sequence_df, scalar, depth, nth_time)

    # Sum everything before last index and add depth of last index
    return sequence_df[:last_index].sum().values[0]*scalar + depth

def find_favourable_runtime_depth(sequence1, sequence2, min_depth=1):
    """


    Note:
    By definition, favourable runtime depth means that:
        CR(sequence1, depth, n) <= CR(sequence2, depth, n) for all n
    Here, this only finds the depth for where n=1.

    Parameters
    =============
    :param sequence1, pd.Series: 
    :param sequence2, pd.Series: 
    :param min_depth, number (optional), the minimium depth 

    Return
    =============
    :return number,  the first favourable runtime time for sequence1 relative to sequence2
        that is greater-or-equal than min_depth

    """

    # TODO: there's probably a way to do this using DP/memoization
    depth = min_depth
    while True:
        # Get first time each sequence reaches 'depth'
        last_index = sequence1.where(sequence1 >= min_depth).first_valid_index()
        if last_index is None:
            raise exceptions.SequenceTooShortException(sequence1, depth)
        sum1 = sequence1[:last_index].sum()

        last_index = sequence2.where(sequence2 >= min_depth).first_valid_index()
        if last_index is None:
            raise exceptions.SequenceTooShortException(sequence2, depth)
        sum2 = sequence2[:last_index].sum()

        if sum1 <= sum2:
            return depth

        depth += 1
        # If the sum is already greater than we know it will be 
        #depth = max(depth + 1, min(series1[last_index], series2[last_index]))


def luby_sequence(time_step, memoized_df=None):
    """

    Return
    =============
    :return Luby(time_step), the time_step-th episode in the luby sequence
    """
    assert time_step > 0, "Invalid input"

    focus = 2
    while (time_step > (focus - 1)):
        focus = focus << 1

    if (time_step == (focus - 1)):
        return focus >> 1
    else:
        return luby_sequence(time_step - (focus >> 1) + 1)


def luby_sequence_df(sequence_length):
    """
    index 0 will be 0, Luby indices start at 1
    """
    df = pd.DataFrame(index=range(sequence_length+1), columns=['luby'])

    df.iloc[0] = 0
    df.iloc[1] = 1

    for time_step in range(2, sequence_length+1):
        focus = 2
        while (time_step > (focus - 1)):
            focus = focus << 1

        if (time_step == (focus - 1)):
            df.iloc[time_step] = focus >> 1
        else:
            df.iloc[time_step] = df.iloc[time_step - (focus >> 1) + 1]

    return df
