import Levenshtein

def search(items, query):
    results = [(item, Levenshtein.ratio(item, query)) for item in items]
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results[0][0]
