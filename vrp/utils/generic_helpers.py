import json
import os


def load_json_file(file_path):
    assert os.path.isfile(file_path)
    with open(file_path) as json_data:
        return json.load(json_data)


def partition(collection, max_parts_count):
    """
    Finds all possible combinations using all elements of the collection.
    # https://stackoverflow.com/a/30134039/1266873
    """

    def _partition(coll):
        if len(coll) == 1:
            yield [coll]
            return

        first = coll[0]
        for smaller in _partition(coll[1:]):
            # insert `first` in each of the subpartition's subsets
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
            # put `first` in its own subset
            yield [[first]] + smaller

    for parts in _partition(collection):
        if len(parts) <= max_parts_count:
            yield parts


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


def print_same_line(text):
    print('\r' + text, end='                                                 ')
