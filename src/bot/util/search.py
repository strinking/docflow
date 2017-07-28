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
                np.add(prev_row[:-1], tgt != s))
        curr_row[1:] = np.minimum(
                curr_row[1:],
                curr_row[0:-1] + 1)
        prev_row = curr_row
    return prev_row[-1]

def ratio(s1, s2):
    if len(s1) > len(s2):
        return levenshtein(s1, s2) / len(s1)
    else:
        return levenshtein(s1, s2) / len(s2)


def search(items, query):
    results = [(item, ratio(item, query)) for item in items]
    print(results)
    sorted_results = sorted(results, key=lambda x: x[1], reverse=False)
    print(sorted_results)
    return sorted_results[0][0]

