"""
Contains extractor functions for
scraped data from cppreference.com.
"""

from typing import Optional, List

import discord

from .cpp_embed import cpp_embed
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

    embed = cpp_embed(stub_)
    for header in stub_['items']:
        embed.add_field(
            name=header,
            value=stub_['items'][header].strip() or "Nothing found here :("
        )
    return embed


def symbol(name: str) -> Optional[List[discord.Embed]]:
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

        return "function"

    def parse_type(symb: dict):
        """Parses a type symbol, such as std::vector."""

        types = '\n'.join(map(
            lambda item: f"{item[0]}: {item[1]}", symb['types'].items()
        ))[1:].replace("[edit]", "")
        funcs = '\n'.join(map(
            lambda item: f"{item[0]}: {item[1]}", symb['funcs'].items()
        ))[1:].replace("(public member function) [edit]", "")

        if len(types) > 1020:
            types = types[:1020] + "..."
        if len(funcs) > 1020:
            funcs = funcs[:1020] + "..."



        embed = cpp_embed(symb)
        embed.add_field(
            name="Member Types",
            value=types
        ).add_field(
            name="Member Functions",
            value=funcs
        )

        return embed

    for symbol_obj in CPP_SYMBOLS:
        # Compatibility with Types
        if any(n == name for n in symbol_obj['names']):
            symb = symbol_obj
            break
    else:
        return None



    response = cpp_embed(symb)
    signature = "```cpp\n" + ''.join(symb['sigs']) + "```"
    if symb['header']:
        backticked_headers = map(lambda header: '`%s`' % header, symb['header'])
        headers = ', '.join(backticked_headers)
    else:
        headers = 'No definition found.'
    response.add_field(
        name="Signature",
        value=signature
    ).add_field(
        name="Defined in Header(s)",
        value=headers
    )

    # Mapping for the symbol types and the parser functions
    members = {
        0: parse_function,
        1: parse_type,
    }[symb['type']](symb)

    return [response, members], symb['type']
