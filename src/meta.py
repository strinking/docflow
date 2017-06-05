"""Houses Meta commands about the Bot, such as uptime or other statistics."""
import discord

from discord.ext import commands
from .run import Bot

SECONDS_IN_A_DAY = 86400


class Meta:
    """Meta Commands with information about the Bot, as well as an invitation link."""
    def __init__(self, bot: Bot):
        self.bot = bot

    def __unload(self):
        pass

    def get_readable_uptime(self) -> str:
        if self.bot.uptime.total_seconds() > SECONDS_IN_A_DAY:
            unit = 'd'
        else:
            unit = 'h'
        return str(self.bot.uptime) + unit

    @commands.command()
    async def uptime(self, ctx):
        """Shows the Bot's uptime as well as its starting time."""
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.blue(),
            description=f'**Uptime**: `{self.get_readable_uptime()}`'
        ))

    @commands.command()
    async def invite(self, ctx):
        """Gives you an invitation link for the Bot."""
        link = ('https://discordapp.com/oauth2/authorize?'
                f'client_id={self.bot.user.id}&scope=bots')
        await ctx.send(embed=discord.Embed(
            title='Invitation Link',
            description=link,
            colour=discord.Colour.blue()
        ))

    @commands.command()
    async def stats(self, ctx):
        """Displays basic stats about the Bot."""
        stats = discord.Embed()
        stats.add_field(
            name='Guilds',
            value=f'Present in {sum(1 for _ in self.bot.guilds)} Guilds'
        ).add_field(
            name='Users',
            value=(f'**Total**: {sum(1 for _ self.bot.users)}\n'
                   f'**Unique**: {sum(1 for _ in set(self.bot.users))}')
        ).add_field(
            name='Uptime',
            value=(f'**Online since**: {self.bot.start_time}\n'
                   f'**Uptime**: {self.get_readable_uptime()}')
        ).colour = discord.Colour.blue()

        await ctx.send(stats)
