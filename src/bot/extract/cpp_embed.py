"""
Contains a subclass of discord.Embed
that aims to reduce a lot of boilerplate
code that was previously used in C++
extraction methods.
"""

import os
print(os.getcwd())
from src.bot import *
import discord


class CppEmbed(discord.Embed):
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

    def __init__(self, cpp_obj: dict, **kwargs):
        super().__init__(**kwargs)
        if 'name' in cpp_obj:
            name = cpp_obj['name']
        else:
            name = ', '.join(cpp_obj['names'])
        self.set_author(
            name="C++: " + name,
            icon_url="http://www.freeiconspng.com/uploads/c--logo-icon-0.png",
            url=cpp_obj['link']
        ).set_footer(
            text="Data from cppreference.com, licensed under CC-BY-SA and GFDL."
        )
        self.colour = discord.Colour.blue()
