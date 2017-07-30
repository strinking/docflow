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
            value=stub['items'][header] or "Nothing found here :("
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

    with open(CPP_SYMBOL_PATH, 'r') as f:
        data = json.load(f)

    for symbol_obj in data:
        if any(n == name for n in symbol_obj['names']):
            symbol = symbol_obj
            break
    else:
        return None

    if symbol["return"] is not None:
        if len(symbol["return"]) >= 150:
            ret_val = None
        else:
            ret_val = symbol["return"][:150].strip()
    else:
        ret_val = symbol["return"]

    return discord.Embed(
        title=f"C++: {', '.join(symbol['names'])}",
        description='\n'.join(symbol['desc']),
        colour=discord.Colour.dark_blue()
    ).set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL.",
    ).add_field(
        name="Signature",
        value="```cpp\n" + ''.join(symbol['sigs']) + "```"
    ).add_field(
        name="Defined in Header(s)",
        value='`' + '`, `'.join(
            symbol['defined_in_header']
        ) + '`' or "No definition found."
    ).add_field(
        name="Parameters",
        value='\n'.join(symbol['params']) or "No parameters found."
    ).add_field(
        name="Return Value",
        value=ret_val or "No non-garbage return value found :("
    ).add_field(
        name="Link",
        value=symbol['link']
    )
