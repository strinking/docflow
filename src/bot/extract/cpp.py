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
import requests

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

    search_result = search(([obj['name'] for obj in data]), query)
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

    def ghost_example(example: str):
        """Posts an example if it exists to ghostbin for 10 minutes"""

        request = requests.post("https://ghostbin.com/paste/new", data={"text" : example, "expire" : "10m", "lang" : "cpp"})
        response.add_field(
            name="Example",
            value=request.url
        )

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

        def member_string(member_dict):
            """Creates a string from a dictionary of member names and descriptions"""

            return '\n'.join("`{k}`: {v}" for k, v in member_dict.items())


        types = member_string(symb['types'])
        funcs = member_string(symb['funcs'])

        response.add_field(
            name="Member Types",
            value=types
        ).add_field(
            name="Member Functions",
            value=funcs
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
    response.add_field(
        name="Signature",
        value="```cpp\n" + ''.join(symb['sigs']) + "```"
    ).add_field(
        name="Defined in Header(s)",
        value='`' + '`, `'.join(
            symb['header']
        ) + '`' or "No definition found."
    )

    if symb["type"] == 0:
        parse_function(symb)
    elif symb["type"] == 1:
        parse_type(symb)
    if symb["example"] != '':
        ghost_example(symb["example"])

    return response
