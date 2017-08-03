"""
Contains a subclass of discord.Embed
that aims to reduce a lot of boilerplate
code that was previously used in C++
extraction methods.
"""

import discord

from ..eval import LANGUAGE_IMAGES


def CppEmbed(symb: dict, **kwargs):
    """
    A basic Embed containing data that is
    the same across all reference Embeds
    sent out.

    As of writing this, this Embed automatically includes:
        - Either a list of names joined on commas, or the
          name of a passed symbol (keys 'name' and 'names')
          with "C++: " prepended to it
        - A link to the original post
        - Reference to cppreference including license notice
        - Dark Blue colour
    """

    embed = discord.Embed(**kwargs)
    if 'name' in symb:
        name = symb['name']
    else:
        name = ', '.join(symb['names'])
    embed.set_author(
        name=f"C++: {name}",
        icon_url=LANGUAGE_IMAGES['cpp'],
        url=symb['link']
    )
    embed.set_footer(
        text="Data from cppreference.com, licensed under CC-BY-SA and GFDL."
    )
    embed.colour = discord.Colour.blue()
    return embed
