"""
Contains extractor functions for
scraped data from cppreference.com.
"""

from typing import Optional

import discord

from .cpp_embed import CppEmbed
from .search import search
from .util import get_ref

CPP_STUBS = get_ref("cpp_stubs.json")
CPP_SYMBOLS = get_ref("cpp_symbols.json")


def stub(query: str) -> Optional[discord.Embed]:
    """
    Searches for the given query in the
    C++ stub database, for example
    "Strings Library".
    """

    names = [obj['name'] for obj in CPP_STUBS]
    search_result = search(names, query)
    for stub_obj in CPP_STUBS:
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
            value=symb['return'] or "Nothing correct values found :("
        )

    def parse_type(symb: dict):
        """Parses a type symbol, such as std::vector."""

        def member_string(member_dict):
            """Creates a string from a dictionary of member names and descriptions"""

            return '\n'.join(f"`{k}`: {v}" for k, v in member_dict.items())

        types = member_string(symb['types'])
        funcs = member_string(symb['funcs'])

        response.add_field(
            name="Member Types",
            value=types
        ).add_field(
            name="Member Functions",
            value=funcs
        )

    for symbol_obj in CPP_SYMBOLS:
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

    {
        0: parse_function,
        1: parse_type,
    }[symb['type']](symb)

    return response
