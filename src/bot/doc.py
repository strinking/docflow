"""Contains the documentation search cog."""

from discord.ext import commands
import extract  # pylint: disable=import-error


class DocSearch:
    """Documentation search commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cppref(self, ctx, symbol: str):
        """Searches the stored data from Cppreference for the given symbol."""

        if not symbol.startswith("std::"):
            symbol = "std::" + symbol

        extracted = extract.cpp_symbol(symbol)
        if extracted is None:
            await ctx.send("Sorry, not found.")
        else:
            await ctx.send(embed=extracted)

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
