"""
Utility module for finding the levenshtein 
distance/ratio between two strings and using it
to search a list for a query
"""
import numpy as np


def levenshtein(src, tgt):
    """returns the levenshtein distance between src and tgt"""
    if len(src) < len(tgt):
        return levenshtein(tgt, src)
    if not tgt:
        return len(src)
    src = np.array(tuple(src))
    tgt = np.array(tuple(tgt))

    prev_row = np.arange(tgt.size + 1)
    for s in src:
        curr_row = prev_row + 1
        curr_row[1:] = np.minimum(
            curr_row[1:],
            np.add(prev_row[:-1], tgt != s)
        )
        curr_row[1:] = np.minimum(
            curr_row[1:],
            curr_row[0:-1] + 1
        )
        prev_row = curr_row
    return prev_row[-1]

def ratio(str1, str2):
    """uses the levenshtein distance between str1 and str2 to find the levenshtein ratio"""
    if len(str1) > len(str2):
        return levenshtein(str1, str2) / len(str1)
    else:
        return levenshtein(str1, str2) / len(str2)


def search(items, query):
    """
    compares a query against every item in a list and finds 
    the lowest levenshtein ratio in order to determine the closest match
    """
    results = [(item, ratio(item, query)) for item in items]
    return min(results, key=lambda r: r[1])[0]
