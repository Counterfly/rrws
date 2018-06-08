import math
import pandas as pd

from helpers import luby_sequence_df, hitting_time_index


def sequence_value_occurence(sequence_df, scalar):
    occurence_map = {}  # could use array too with gaps
    column_name = list(sequence_df)[0]
    for _, row in sequence_df.iterrows():
        value = row[column_name] * scalar
        if value not in occurence_map:
            occurence_map[value] = 0
        occurence_map[value] += 1

    return occurence_map


def aggregate_sum(mapping):
    print("max is ", max(mapping.keys()))
    l = [0] * (max(mapping.keys()) + 1)
    for value in mapping.keys():
        num_occurrences = mapping[value]
        for i in range(1, value+1):
            l[i] += num_occurrences

    return l

def main(l1, l2, depth, n):
    """
    l1,l2 scalars for luby sequence
    depth, depth the algorithm terminates at
    n, the nth time depth 'depth' is reached when it terminates
    """
    luby_df = luby_sequence_df(1000)

    last_index_l1 = hitting_time_index(luby_df, l1, depth, n)
    last_index_l2 = hitting_time_index(luby_df, l2, depth, n)

    l1_mapping = sequence_value_occurence(luby_df[:last_index_l1 + 1], l1)
    l2_mapping = sequence_value_occurence(luby_df[:last_index_l2 + 1], l2)

    print(l1_mapping)
    print(l2_mapping)

    l1_sums = aggregate_sum(l1_mapping)
    l2_sums = aggregate_sum(l2_mapping)

    # fix sums because it necessarily didn't go to the end of the last episode
    print(range(depth + 1, int(luby_df.iloc[last_index_l1][0]) * l1 + 1))
    for i in range(depth + 1, int(luby_df.iloc[last_index_l1][0]) * l1):
        l1_sums[i] -= 1

    print(range(depth + 1, int(luby_df.iloc[last_index_l2][0]) * l2))
    for i in range(depth + 1, int(luby_df.iloc[last_index_l2][0]) * l2 + 1):
        l2_sums[i] -= 1

    # Convert to a dataframe bc it looks nicer
    # First fill in the arrays so same length
    if len(l1_sums) > len(l2_sums):
        l2_sums += [0] * (len(l1_sums) - len(l2_sums))
    else:
        l1_sums += [0] * (len(l2_sums) - len(l1_sums))

    result = pd.DataFrame({ 'l1': l1_sums, 'l2': l2_sums })
    print(result)

    mask = result['l1'] >= result['l2']
    conjunction = True
    for _, row in mask.iteritems():
        conjunction = conjunction and row



    l1_luby = []
    l2_luby = []
    import helpers
    for i in range(1, 40):
        value = helpers.luby_sequence(i)
        l1_luby.append(value * l1)
        l2_luby.append(value * l2)
    print(l1_luby)
    print(l2_luby)
    print("=" * 10)
    print(conjunction)




if __name__ == '__main__':
    l1 = 2
    l2 = 3
    depth = 4
    n = 2
    main(l1, l2, depth, n)
