import numpy as np


def levenshtein(src, tgt):
    if len(src) < len(tgt):
        return levenshtein(tgt, src)
    if len(tgt) == 0:
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


def ratio(a, b):  # pylint: disable=invalid-name
    if len(a) > len(b):
        return levenshtein(a, b) / len(a)
    return levenshtein(a, b) / len(b)


def search(items, query):
    results = [(item, ratio(item, query)) for item in items]
    return min(results, key=lambda r: r[1])[0]
