import datetime
import discord

from discord.ext import commands

DESCRIPTION = 'Hello! I am a Bot providing code evaluation and documentation search.'


class Bot(commands.AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.start_time = datetime.datetime.utcnow()

    @property
    def uptime(self) -> datetime.timedelta:
        return datetime.datetime.utcnow() - self.start_time

    async def on_ready(self):
        pass

    async def on_command_error(self, ctx, error):
        async def send_error(description):
            await ctx.send(embed=discord.Embed(
                description=description,
                colour=discord.Colour.red()
            ))

        if isinstance(error, commands.MissingRequiredArgument):
            error_msg = ('You are missing the parameter '
                         f'{error.param} for the Command.')
            await send_error(error_msg)
        elif isinstance(error, commands.NoPrivateMessage):
            error_msg = 'This Command cannot be used in Private Messages.'
            await send_error(error_msg)
        elif isinstance(error, commands.BadArgument):
            error_msg = ('You invoked the Command with the wrong type of '
                         'arguments. Use `.help <command>` to get'
                         'information about its usage.')
            await send_error(error_msg)
        elif isinstance(error, commands.CommandInvokeError):
            owner = self.get_user(self.owner_id)
            await owner.send(embed=discord.Embed(
                title=f'Exception in command `{ctx.message.content}`',
                description=error.original,
                colour=discord.Colour.red()
            ))
        elif isinstance(error, commands.CommandNotFound):
            pass


if __name__ == '__main__':
    bot = Bot(command_prefix='.', description=DESCRIPTION, pm_help=None)

