import os
import json
from collections import defaultdict


def get_input(input_file_name):
    assert os.path.isfile(input_file_name)
    with open(input_file_name) as json_data:
        return json.load(json_data)


def partition(collection):
    """
    Finds all possible combinations using all elements of the collection.
    https://stackoverflow.com/a/30134039/1266873
    """
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
        # put `first` in its own subset
        yield [[first]] + smaller


def lists_overlap(a, b):
    """
    Checks if two lists have at least one common element.
    https://stackoverflow.com/a/17735466/1266873
    """
    return not frozenset(a).isdisjoint(b)


def calculate_route_distance(route, matrix):
    dist = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        dist += matrix[pre_index][index]
    return dist


def calculate_all_routes_distance(routes, matrix):
    return sum([calculate_route_distance(route, matrix) for route in routes])


# def _route_has_distance_more_than(route, matrix, distance):
#     dist = 0
#     pre_index = route[0]
#     for i in range(1, len(route)):
#         index = route[i]
#         dist += matrix[pre_index][index]
#         if dist > distance:
#             return True, None
#     return False, dist


def routes_distance_is_smaller_than(routes, matrix, distance):
    dist = 0
    for route in routes:
        pre_index = route[0]
        for i in range(1, len(route)):
            index = route[i]
            dist += matrix[pre_index][index]
            if dist >= distance:
                return False, None
    return True, dist
    # dist = distance
    # for route in routes:
    #     is_more, dist1 = _route_has_distance_more_than(route, matrix, dist)
    #     if is_more:
    #         return True
    #     dist -= dist1
    # return False


def print_same_line(text):
    print('\r' + text, end='')
