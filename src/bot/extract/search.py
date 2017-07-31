"""
Utility module for finding the Levenshtein
distance/ratio between two strings and using
it to search a list for a query
"""

import numpy as np


def levenshtein(source, target):
    """Returns the Levenshtein distance between source and target"""

    if len(source) < len(target):
        return levenshtein(target, source)
    if not target:
        return len(source)
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    prev_row = np.arange(target.size + 1)
    for src in source:
        curr_row = prev_row + 1
        curr_row[1:] = np.minimum(  # pylint: disable=no-member
            curr_row[1:],
            np.add(prev_row[:-1], target != src)
        )
        curr_row[1:] = np.minimum(  # pylint: disable=no-member
            curr_row[1:],
            curr_row[0:-1] + 1
        )
        prev_row = curr_row
    return prev_row[-1]


def ratio(a, b):  # pylint: disable=invalid-name
    """Uses the Levenshtein distance between a and b to find the Levenshtein ratio"""

    return levenshtein(a, b) / max(len(a), len(b))


def search(items, query):
    """
    Compares a query against every item in a list and finds
    the lowest Levenshtein ratio in order to determine the closest match
    """

    return min(((item, ratio(item, query)) for item in items), key=lambda r: r[1])[0]
