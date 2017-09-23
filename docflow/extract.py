"""
This module is used to
search through and extract
documentation downloaded
to the `data` directory,
stored as markdown.
Each language directory
supplies an index JSON
file which is used for
fuzzy searching.
"""

import os
import json
from operator import itemgetter

from fuzzywuzzy import fuzz


def get_data_subdirs():
    """
    Yields each directory
    in the `data` directory.
    """

    return (d for d in os.listdir('data')
            if os.path.isdir(os.path.join('data', d)))


def get_lang_dir(lang_name):
    """
    Fuzzy searches the data
    directory for the language
    directory with the given
    language name.
    """

    lang_gen = ifuzzy(lang_name, get_data_subdirs())
    match_lang = max(lang_gen, key=itemgetter(0))
    return os.path.join('data', match_lang[1])


def ifuzzy(name, seq, key=lambda e: e):
    """
    A helper function which
    yields the fuzzy ratio
    applied onto the key of
    the given element and the
    given name onto each
    element of the given
    sequence as well as
    the element itself.
    """

    for elem in seq:
        yield fuzz.ratio(key(elem), name), elem


def get_best_symbol_match(entries, name):
    """
    Attempts to get the best symbol
    by searching through all entries
    from the language database.
    """

    match = max(ifuzzy(name, entries, itemgetter('name')), key=itemgetter(0))
    return match[1]


def get_symbol_path(lang_dir, name):
    """
    Returns the path to the symbol
    with the given name, specified
    in the `index.json` file for each
    language subdirectory. The
    symbol passed by `name` is
    used to fuzzily search through
    the entries in `index.json`.
    """

    with open(os.path.join(lang_dir, "index.json")) as index_file:
        data = json.load(index_file)
    match = get_best_symbol_match(data['entries'], name)
    return match['path']


def search(lang, name) -> str:
    """
    Searches for the given symbol
    in the given language.
    Both are fuzzily searched
    from the subdirectories in the
    `data` directory. Afterwards,
    this reads the Markdown file
    specified under the path
    returned by `get_symbol_path`
    and returns the full contents
    of the file.
    """

    lang_dir = get_lang_dir(lang)
    item_path = get_symbol_path(lang_dir, name)
    full_path = os.path.join(lang_dir, item_path)
    with open(full_path + '.md') as symbol_md:
        return symbol_md.read()
