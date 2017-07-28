"""
The functions defined in this module extract the documentation from various
reference documents and returns them in Embeds, ready to be sent.
"""
import discord
import os
import json
from search import search
from typing import Optional


CPP_SYMBOL_PATH = os.path.join(os.path.abspath(
    os.path.pardir), 'doc', "cpp_symbols.json")
CPP_STUB_PATH = os.path.join(os.path.abspath(os.path.pardir), 'doc', 'stub.json') 

def cpp_stub(query: str) -> discord.Embed:
    with open(CPP_STUB_PATH, 'r') as f:
        data = json.load(f)
    
    names = [obj["name"] for obj in data]
    search_result = search(names, query)
    for stub_obj in data:
        if any(n == search_result for n in stub_obj["name"]):
            stub = stub_obj
            break
        else:
            return None
    return discord.Embed(
        title=stub['name'],
        description=stub['items_raw'][0],
        colour=discord.Colour.dark_blue()
    ).set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL."
    ).add_field(
        name="Defined in Header(s)",
        value="```cpp\n" + ';\n'.join(stub['defined_in_header']) + "```"
    ).add_field(
        name="Link",
        value=stub["link"]
    )


def cpp_symbol(name: str) -> Optional[discord.Embed]:
    with open(CPP_SYMBOL_PATH, 'r') as f:
        data = json.load(f)

    names = [obj["name"] for obj in data]
    search_result = search(names, name)

    for symbol_obj in data:
        if any(n == search_result for n in symbol_obj['names']):
            symbol = symbol_obj
            break
    else:
        return None

    return discord.Embed(
        title=f"C++: {', '.join(symbol['names'])}",
        description='\n'.join(symbol['desc']),
        colour=discord.Colour.dark_blue()
    ).set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL.",
    ).add_field(
        name="Signature",
        value="```cpp\n" + ';\n'.join(symbol['sigs']) + "```"
    ).add_field(
        name="Defined in Header(s)",
        value='`' + '`, `'.join(symbol['defined_in_header']) + '`' or "No definition found."
    ).add_field(
        name="Parameters",
        value='\n'.join(symbol['params']) or "No parameters found."
    ).add_field(
        name="Link",
        value=symbol['link']
    )
