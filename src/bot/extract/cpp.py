"""
Contains extractor functions for
scraped data from cppreference.com.
"""

import json
from typing import Optional
from .search import search

import discord

from util import get_ref_path


CPP_STUB_PATH = get_ref_path("cpp_stubs.json")
CPP_SYMBOL_PATH = get_ref_path("cpp_symbols.json")


def stub(query: str) -> Optional[discord.Embed]:
    """
    Searches for the given query in the
    C++ stub database, for example
    "Strings Library".
    """

    with open(CPP_STUB_PATH, 'r') as f:
        data = json.load(f)

    names = [obj['name'] for obj in data]
    search_result = search(names, query)
    for stub_obj in data:
        if search_result == stub_obj['name']:
            stub = stub_obj
            break
    else:
        return None

    embed = discord.Embed(
        title=stub['name'],
        colour=discord.Colour.dark_blue()
    )

    for header in stub['items']:
        embed.add_field(
            name=header,
            value=stub['items'][header].strip() or "Nothing found here :("
        )
    embed.set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL."
    ).add_field(
        name="Link",
        value=stub['link']
    )

    return embed


def symbol(name: str) -> Optional[discord.Embed]:
    """
    Extracts the given C++ symbol from the
    C++ symbol index, for example std::cout.
    """

    response = discord.Embed()

    def parse_function(symbol: dict):
        response.add_field(
            name="Parameters",
            value='\n'.join(symbol['params']) or "No parameters found."
        ).add_field(
            name="Return Value",
            value=symbol['return'] or "No non-garbage return value found :("
        )

    def parse_type(symbol: dict):
        response.add_field(
            name="Member Types",
            value=symbol['types']
        ).add_field(
            name="Member Functions",
            value=symbol['funcs']
        )

    with open(CPP_SYMBOL_PATH, 'r') as f:
        data = json.load(f)

    for symbol_obj in data:
        # Compatibility with Types
        if any(n == name for n in symbol_obj['names']):
            symbol = symbol_obj
            break
    else:
        return None

    response.title = f"C++: {', '.join(symbol['names'])}"
    response.description = '\n'.join(symbol['desc'])
    response.colour = discord.Colour.dark_blue()
    response.set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL."
    ).add_field(
        name="Signature",
        value="```cpp\n" + ''.join(symbol['sigs']) + "```"
    ).add_field(
        name="Defined in Header(s)",
        value='`' + '`, `'.join(
            symbol['header']
        ) + '`' or "No definition found."
    )

    if symbol["type"] == 0:
        parse_function(symbol)
    elif symbol["type"] == 1:
        parse_type(symbol)

    return response
