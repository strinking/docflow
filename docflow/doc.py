"""Contains the documentation search cog."""

from discord.ext import commands
from . import extract
from .lce import LongContentEmbed


class DocSearch:
    """Documentation search commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cref(self, ctx, *, symbol: str):
        """Searches the stored data from Cppreference for the given symbol."""

        extracted = extract.search('c', symbol)
        embed = LongContentEmbed(extracted, "C Reference",
                                 0x555, ctx.message.author.id)
        await embed.send(ctx, self.bot)

    @commands.command()
    async def cppref(self, ctx, *, symbol: str):
        """Searches the stored data from Cppreference for the given symbol."""

        extracted = extract.search('cpp', symbol)
        embed = LongContentEmbed(extracted, "C++ Reference",
                                 0xf34b7d, ctx.message.author.id)
        await embed.send(ctx, self.bot)

    @commands.command()
    async def pydoc(self, ctx, *, symbol: str):
        """Searches the stored data from Python 3.6 for the given symbol."""

        extracted = extract.search('python', symbol)
        embed = LongContentEmbed(extracted, "Python 3 Documentation",
                                 0x3581ba, ctx.message.author.id)
        await embed.send(ctx, self.bot)

    @commands.command()
    async def mangit(self, ctx, *, subcommand: str):
        """Searches the database for the given git subcommand docs."""

        extracted = extract.search('git', subcommand)
        embed = LongContentEmbed(extracted, "Git Manpages",
                                 0xea4b33, ctx.message.author.id)
        await embed.send(ctx, self.bot)


def setup(bot):
    """Adds the Documentation Search cog to the Bot."""

    bot.add_cog(DocSearch(bot))
