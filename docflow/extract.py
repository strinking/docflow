import os
import json
from operator import itemgetter
from typing import Optional

from fuzzywuzzy import fuzz

from ..util.paged_embed import PagedEmbed


def get_data_subdirs():
    return (d for d in os.listdir('data')
            if os.path.isdir(os.path.join('data', d)))


def get_lang_dir(lang_name):
    lang_gen = ifuzzy(lang_name, get_data_subdirs())
    match_lang = max(lang_gen, key=itemgetter(0))
    return os.path.join('data', match_lang[1])


def ifuzzy(name, seq, key=lambda e: e):
    for elem in seq:
        yield fuzz.ratio(key(elem), name), elem


def get_best_symbol_match(entries, name):
    match = max(ifuzzy(name, entries, itemgetter('name')), key=itemgetter(0))
    return match[1]


def get_symbol_path(lang_dir, name):
    with open(os.path.join(lang_dir, "index.json")) as f:
        data = json.load(f)
    match = get_best_symbol_match(data['entries'], name)
    return match['path']


def search(lang, name) -> Optional[PagedEmbed]:
    lang_dir = get_lang_dir(lang)
    item_path = get_symbol_path(lang_dir, name)
    full_path = os.path.join(lang_dir, item_path)
    with open(full_path + '.md') as f:
        return f.read()
