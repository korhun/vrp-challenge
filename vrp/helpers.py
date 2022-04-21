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


def lists_overlap_count(a, b):
    """
    Finds two lists' common elements count
    https://stackoverflow.com/a/4775027/1266873
    """
    return len(frozenset(a) & frozenset(b))


def calculate_route_cost(route, matrix):
    dist = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        dist += matrix[pre_index][index]
    return dist


def calculate_all_routes_costs(routes, matrix):
    return sum([calculate_route_cost(route, matrix) for route in routes])


def routes_cost_is_smaller_than(routes, matrix, cost):
    dist = 0
    for route in routes:
        pre_index = route[0]
        for i in range(1, len(route)):
            index = route[i]
            dist += matrix[pre_index][index]
            if dist >= cost:
                return False, None
    return True, dist


def route_cost_is_more_than(route, matrix, cost):
    total = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        total += matrix[pre_index][index]
        if total > cost:
            return True
    return True


def build_location_to_delivery(jobs):
    tuples = []
    for job in jobs:
        tuples.append((job["location_index"], job["delivery"][0]))
    return dict(tuples)


def build_location_to_job(jobs):
    tuples = []
    for job in jobs:
        tuples.append((job["location_index"], job))
    return dict(tuples)


def print_same_line(text):
    print('\r' + text, end='                                                 ')
