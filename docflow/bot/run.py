"""The entry point for the Bot."""

import datetime
import os
import traceback
import sys

import discord
from discord.ext import commands

DESCRIPTION = 'Hello! I am a Bot providing code eval and documentation search.'
START_FAIL_MSG = """
Failed to start the Bot.
Please set an environment variable named DISCORD_TOKEN
as described in README.md which the bot can use to login.
"""
COGS_ON_LOGIN = [
    'admin',
    'doc',
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

    @staticmethod
    async def on_command_error(ctx, error):  # pylint: disable=arguments-differ
        """Handles all errors returned from Commands."""

        async def send_error(description):
            """A small helper function which sends an Embed with red colour."""

            await ctx.send(embed=discord.Embed(
                description=description,
                colour=discord.Colour.red()
            ))

        if isinstance(error, commands.MissingRequiredArgument):
            await send_error(
                f'You are missing the parameter {error.param} for the Command.'
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await send_error(
                'This Command cannot be used in Private Messages.'
            )
        elif isinstance(error, commands.BadArgument):
            await send_error(
                'You invoked the Command with the wrong type of arguments. Use'
                '`.help <command>` to get information about its usage.'
            )
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title='Exception in command occurred, traceback printed.',
                colour=discord.Colour.red()
            ))
            print(
                'In {0.command.qualified_name}:'.format(ctx),
                file=sys.stderr
            )
            traceback.print_tb(error.original.__traceback__)
            print(
                '{0.__class__.__name__}: {0}'.format(error.original),
                file=sys.stderr
            )
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(
                title='This Command is currently on cooldown.',
                colour=discord.Colour.red()
            ))
        elif isinstance(error, commands.CommandNotFound):
            pass


def start():
    """
    Starts the bot.

    Instead of calling this function
    from another script, it is also possible
    to simply execute this file, as the main
    function will simply call this function.
    """

    BOT = Bot(command_prefix='.', description=DESCRIPTION, pm_help=None)

    for cog in COGS_ON_LOGIN:
        BOT.load_extension("docflow.bot." + cog)

    if 'DISCORD_TOKEN' in os.environ:
        BOT.run(os.environ['DISCORD_TOKEN'])
    else:
        print(START_FAIL_MSG)


if __name__ == '__main__':
    start()
