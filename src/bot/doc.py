"""Contains the documentation search cog."""

import os
import discord

from discord.ext import commands
import extract  # pylint: disable=import-error


class DocSearch:
    """Documentation search commands."""

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_doc_path(ref_name: str):
        """Gets the full path to the specified documentation file."""

        return os.path.join(
            os.path.abspath(os.path.pardir), "docflow", "data", ref_name
        )

    def ref_exists(self, ref_name: str):
        """Checks if the given reference document exists."""

        return os.path.exists(self.get_doc_path(ref_name))

    @staticmethod
    async def send_notice_no_ref_found(ctx: commands.Context, ref_name: str):
        """Sends a notice indicating that the requested reference file was not found."""

        await ctx.send(embed=discord.Embed(
            title=f"Failed to lookup documentation for {ref_name}",
            description=("No reference file was found. The bot administrator "
                         "must run scrapy in order for this Command to work."),
            colour=discord.Colour.red()
        ))

    @commands.command()
    async def cppref(self, ctx, symbol: str):
        """Searches the stored data from Cppreference for the given symbol."""

        if not symbol.startswith("std::"):
            symbol = "std::" + symbol

        if not self.ref_exists("cpp_symbols.json"):
            return await self.send_notice_no_ref_found(ctx, "C++")

        extracted = extract.cpp_symbol(symbol)
        if extracted is None:
            await ctx.send("Sorry, not found.")
        else:
            await ctx.send(embed=extracted)

    @commands.command()
    async def cppstub(self, ctx, *, query: str):
        """Searches the database for C++ stubs and returns the closest item"""

        if not self.ref_exists("cpp_stubs.json"):
            return await self.send_notice_no_ref_found(ctx, "C++")

        extracted = extract.cpp_stub(query)
        if extracted is None:
            await ctx.send("Sorry, not found.")
        else:
            await ctx.send(embed=extracted)


def setup(bot):  # pylint: disable=missing-docstring
    bot.add_cog(DocSearch(bot))
