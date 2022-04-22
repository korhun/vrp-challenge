import os
import json


def load_json_file(file_path):
    assert os.path.isfile(file_path)
    with open(file_path) as json_data:
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
    """
    return not frozenset(a).isdisjoint(b)


def lists_overlap_count(a, b):
    """
    Finds two lists' common elements count
    """
    return len(frozenset(a) & frozenset(b))


def calculate_route_cost(route, matrix, service_times):
    total = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        total += matrix[pre_index][index]
        if service_times is not None:
            total += service_times[index]
        pre_index = index
    return total


def calculate_all_routes_costs(routes, matrix, service_times):
    return sum([calculate_route_cost(route, matrix, service_times) for route in routes])


def routes_cost_is_less_than(routes, matrix, cost, service_times):
    total = 0
    for route in routes:
        pre_index = route[0]
        for i in range(1, len(route)):
            index = route[i]
            total += matrix[pre_index][index]
            if service_times is not None:
                total += service_times[index]
            if total >= cost:
                return False, None
            pre_index = index
    return True, total


def route_costs_less_than(route, matrix, cost, service_times):
    """
    :return: (False, None) if route costs less than 'cost' else (True, cost value of the route)
    """
    total = 0
    pre_index = route[0]
    for i in range(1, len(route)):
        index = route[i]
        total += matrix[pre_index][index]
        if service_times is not None:
            total += service_times[index]
        if total > cost:
            return False, None
        pre_index = index
    return True, total


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


def build_location_to_job_service_times(jobs):
    tuples = []
    for job in jobs:
        tuples.append((job["location_index"], job["service"]))
    return dict(tuples)


def build_location_to_vehicle(vehicles):
    tuples = []
    for vehicle in vehicles:
        tuples.append((vehicle["start_index"], vehicle))
    return dict(tuples)


def print_same_line(text):
    print('\r' + text, end='                                                 ')
