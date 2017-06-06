"""The entry point for the Bot."""

import datetime
import os

import discord
from discord.ext import commands

DESCRIPTION = 'Hello! I am a Bot providing code evaluation and documentation search.'
DISCORD_TOKEN = ''
START_FAIL_MSG = """
Failed to start the Bot. You have the following options for starting it:
- Use an environment variable called DISCORD_TOKEN.
    Doing this with a virtual environment is explained in the README.md.
- Set the variable DISCORD_TOKEN in `run.py` to your token.
    Not recommended, as you might commit it by accident.
- Create a file called `token.txt` containing just your token.
    You can make Git ignore this file by using 
    `git update-index --assume-unchanged token.txt`. To revert, use 
    `--no-assume-unchanged`.'
"""
COGS_ON_LOGIN = [
    'admin',
    'eval',
    'meta'
]


class Bot(commands.AutoShardedBot):
    """
    A subclass of Discord's Bot to provide additional attributes
    such as uptime.
    """

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.start_time = datetime.datetime.utcnow()

    @property
    def uptime(self) -> datetime.timedelta:
        """Returns a fresh calculation of the Bot's uptime."""
        return datetime.datetime.utcnow() - self.start_time

    @staticmethod
    async def on_ready():
        """The on_ready Event, emitted by Discord."""
        print('Logged in.')

    async def on_command_error(self, ctx, error):
        """Handles all errors returned from Commands."""
        async def send_error(description):
            """A small helper function which sends an Embed with red colour."""
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
            if owner is not None:
                destination = owner
            else:
                destination = ctx.channel
            await destination.send(embed=discord.Embed(
                title=f'Exception in command `{ctx.message.content}`',
                description=error.original,
                colour=discord.Colour.red()
            ))
        elif isinstance(error, commands.CommandNotFound):
            pass


if __name__ == '__main__':
    BOT = Bot(command_prefix='.', description=DESCRIPTION, pm_help=None)

    for cog in COGS_ON_LOGIN:
        BOT.load_extension(cog)

    if 'DISCORD_TOKEN' in os.environ:
        BOT.run(os.environ['DISCORD_TOKEN'])
    elif DISCORD_TOKEN != '':
        BOT.run(DISCORD_TOKEN)
    elif os.path.exists(os.path.join(os.getcwd(), 'token.txt')):
        with open('token.txt', 'r') as f:
            BOT.run(f.read())
    else:
        print(START_FAIL_MSG)
