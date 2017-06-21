"""Contains functions to administrate the Bot."""
import discord

from discord.ext import commands


PERMITTED_USERS = [
    196989358165852160,  # Volcyy
    98633956773093376,  # Mallard
    130012001236811776,  # Maware
    155267292047867904,  # Hatefrog
    197177484792299522  # Aeshthetic
]


def is_permitted(ctx: commands.Context):
    return ctx.author.id in PERMITTED_USERS


class Admin:
    """Commands for administrating the Bot."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_permitted)
    async def shutdown(self, ctx):
        """Shut the Bot down."""
        await ctx.send(embed=discord.Embed(
            title='Shutting down...',
            colour=discord.Colour.blue()
        ))
        await self.bot.close()

    @commands.command()
    @commands.check(is_permitted)
    async def reloadall(self, ctx):
        """Reload all currently loaded Cogs."""
        # Cast to list to prevent a RuntimeError, since we just want the iteration for the names of the Cogs
        for extension_name in list(self.bot.extensions):
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)

        await ctx.send(embed=discord.Embed(
            title='Reload Complete',
            description=f'Reloaded {len(self.bot.cogs)} Cogs.',
            colour=discord.Colour.green()
        ))

    @commands.command()
    @commands.check(is_permitted)
    async def reload(self, ctx, *, cog_name: str):
        """Reloads a single Cog."""
        cog_name = cog_name.title()
        if cog_name not in self.bot.cogs:
            await ctx.send(embed=discord.Embed(
                title=f'No Cog named `{cog_name}` currently loaded or found.',
                colour=discord.Colour.red()
            ))
        else:
            self.bot.remove_cog(cog_name)
            self.bot.unload_extension(cog_name.lower())
            self.bot.load_extension(cog_name.lower())
            await ctx.send(embed=discord.Embed(
                title=f'Reloaded Cog {cog_name}.',
                colour=discord.Colour.green()
            ))

    @commands.command()
    @commands.check(is_permitted)
    async def load(self, ctx, *, cog_name: str):
        """Load a Cog."""
        cog_name = cog_name.title()
        if cog_name in self.bot.cogs:
            await ctx.send(embed=discord.Embed(
                title=f'Cog `{cog_name}` is already loaded.',
                colour=discord.Colour.red()
            ))
        else:
            try:
                self.bot.load_extension(cog_name.lower())
            except (ModuleNotFoundError, TypeError) as err:
                await ctx.send(embed=discord.Embed(
                    title=f'Failed to load {cog_name}:',
                    description=str(err),
                    colour=discord.Colour.red()
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    title=f'Loaded the {cog_name} Cog.',
                    colour=discord.Colour.green()
                ))

    @commands.command()
    @commands.check(is_permitted)
    async def unload(self, ctx, *, cog_name: str):
        """Unload a Cog."""
        cog_name = cog_name.title()
        if cog_name not in self.bot.cogs:
            await ctx.send(embed=discord.Embed(
                title=f'No Cog named `{cog_name}` currently loaded or found.',
                colour=discord.Colour.red()
            ))
        else:
            self.bot.remove_cog(cog_name)
            self.bot.unload_extension(cog_name.lower())
            await ctx.send(embed=discord.Embed(
                title=f'Unloaded the {cog_name} Cog.',
                colour=discord.Colour.green()
            ))


def setup(bot):
    bot.add_cog(Admin(bot))
