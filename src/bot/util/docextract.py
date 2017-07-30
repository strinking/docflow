"""
The functions defined in this module extract the documentation from various
reference documents and returns them in Embeds, ready to be sent.
"""
import os
import json
from typing import Optional
from .search import search

import discord


CPP_SYMBOL_PATH = os.path.join(
    os.path.abspath(os.path.pardir), "docflow", "doc", "cpp_symbols.json"
)
CPP_STUB_PATH = os.path.join(
    os.path.abspath(os.path.pardir), "docflow", "doc", "cpp_stubs.json"
)


def cpp_stub(query: str) -> Optional[discord.Embed]:
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


def cpp_symbol(name: str) -> Optional[discord.Embed]:
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
        pass

    with open(CPP_SYMBOL_PATH, 'r') as f:
        data = json.load(f)

    for symbol_obj in data:
        # Compatibility with Types
        if any(n == name for n in symbol_obj.get('names', 'name')):
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
