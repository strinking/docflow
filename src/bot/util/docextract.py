"""
The functions defined in this module extract the documentation from various
reference documents and returns them in Embeds, ready to be sent.
"""
import discord
import os
import json

from typing import Optional


CPP_SYMBOL_PATH = os.path.join(os.path.abspath(os.path.pardir), 'docflow', 'doc', "symbols.json")


def cpp_symbol(name: str) -> Optional[discord.Embed]:
    with open(CPP_SYMBOL_PATH, 'r') as f:
        data = json.load(f)

    for symbol_obj in data:
        if any(n == name for n in symbol_obj['names']):
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
        name="Defined in Header(s)",
        value='`' + '`, `'.join(symbol['defined_in_header']) + '`' or "No definition found."
    ).add_field(
        name="Signature",
        value="```cpp\n" + ';\n'.join(symbol['sigs']) + "```"
    ).add_field(
        name="Parameters",
        value='\n'.join(symbol['params']) or "No parameters found."
    ).add_field(
        name="Link",
        value=symbol['link']
    )
