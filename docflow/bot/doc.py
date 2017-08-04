"""Contains the documentation search cog."""

from discord.ext import commands
from . import extract
from .util.paged_embed import PagedEmbed


class DocSearch:
    """Documentation search commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cppref(self, ctx, symbol: str):
        """Searches the stored data from Cppreference for the given symbol."""

        if not symbol.startswith("std::"):
            symbol = "std::" + symbol

        extracted, symbol_type = extract.cpp_symbol(symbol)
        if extracted is None:
            await ctx.send("Sorry, not found.")
        else:
            if symbol_type == 1:
                embed = PagedEmbed(ctx, self.bot, "🍏", extracted[0])
                embed.add_page("💛", extracted[1])
                await embed.send()
            elif symbol_type == 0:
                embed = extracted[0]
                await ctx.send(embed=embed)

    @commands.command()
    async def cppstub(self, ctx, *, query: str):
        """Searches the database for C++ stubs and returns the closest item"""

        extracted = extract.cpp_stub(query)
        if extracted is None:
            await ctx.send("Sorry, not found.")
        else:
            await ctx.send(embed=extracted)


def setup(bot):
    """Adds the Administration cog to the Bot."""

    bot.add_cog(DocSearch(bot))
