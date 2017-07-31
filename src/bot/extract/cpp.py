"""
Contains extractor functions for
scraped data from cppreference.com.
"""

import json
from typing import Optional

import discord

from .cpp_embed import CppEmbed
from .search import search
from .util import get_ref_path

CPP_STUB_PATH = get_ref_path("cpp_stubs.json")
CPP_SYMBOL_PATH = get_ref_path("cpp_symbols.json")


def stub(query: str) -> Optional[discord.Embed]:
    """
    Searches for the given query in the
    C++ stub database, for example
    "Strings Library".
    """

    with open(CPP_STUB_PATH, 'r') as file:
        data = json.load(file)

    names = [obj['name'] for obj in data]
    search_result = search(names, query)
    for stub_obj in data:
        if search_result == stub_obj['name']:
            stub_ = stub_obj
            break
    else:
        return None

    embed = CppEmbed(stub_)
    for header in stub_['items']:
        embed.add_field(
            name=header,
            value=stub_['items'][header].strip() or "Nothing found here :("
        )
    return embed


def symbol(name: str) -> Optional[discord.Embed]:
    """
    Extracts the given C++ symbol from the
    C++ symbol index, for example std::cout.
    """

    def parse_function(symb: dict):
        """Parses a function symbol, such as std::abs."""

        response.add_field(
            name="Parameters",
            value='\n'.join(symb['params']) or "No parameters found."
        ).add_field(
            name="Return Value",
            value=symb['return'] or "No non-garbage return value found :("
        )

    def parse_type(symb: dict):
        """Parses a type symbol, such as std::vector."""

        response.add_field(
            name="Member Types",
            value=symb['types']
        ).add_field(
            name="Member Functions",
            value=symb['funcs']
        )

    with open(CPP_SYMBOL_PATH, 'r') as file:
        data = json.load(file)

    for symbol_obj in data:
        # Compatibility with Types
        if any(n == name for n in symbol_obj['names']):
            symb = symbol_obj
            break
    else:
        return None

    response = CppEmbed(symb)
    signature = "```cpp\n" + ''.join(symb['sigs']) + "```"
    headers = '`' + '`, `'.join(symb['header']) + '`' or "No definition found."
    response.add_field(
        name="Signature",
        value=signature
    ).add_field(
        name="Defined in Header(s)",
        value=headers
    )

    if symb["type"] == 0:
        parse_function(symb)
    elif symb["type"] == 1:
        parse_type(symb)

    return response
