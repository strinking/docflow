"""Houses Meta commands about the Bot, such as uptime or other statistics."""
import discord

from discord.ext import commands
from .run import Bot

SECONDS_IN_A_DAY = 86400


class Meta:
    """Meta Commands with information about the Bot."""
    def __init__(self, bot: Bot):
        self.bot = bot

    def __unload(self):
        pass

    @commands.command()
    async def uptime(self, ctx):
        """Shows the Bot's uptime as well as its starting time."""
        if self.bot.uptime.total_seconds() > SECONDS_IN_A_DAY:
            unit = 'd'
        else:
            unit = 'h'
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.blue(),
            description=f'**Uptime**: `{self.bot.uptime}`{unit}'
        ))
