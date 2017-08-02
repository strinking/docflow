import discord
from discord.ext import commands


class EmbedPage(discord.Embed):
    pass


class PagedEmbed:
    def __init__(self, ctx, bot: commands.Bot, *args, **kwargs):
        self._ctx = ctx
        self._bot = bot
        # Dictionary to contain embed Pages in the following format:
        #   {
        #       "default": EmbedPage,
        #       "emoji_id": EmbedPage,
        #       "emoji_id": EmbedPage,
        #       ...
        #   }
        self._pages = {
            'default': EmbedPage(*args, **kwargs)
        }
        self.current_page = self._pages['default']

        # Attach our event listeners to the bot
        self._bot.add_listener(self.on_reaction_add)
        self._bot.add_listener(self.on_reaction_remove)

    async def add_page(self, emoji: discord.Emoji, page: EmbedPage):
        pass

    async def send(self):
        await self._ctx.send(embed=self.current_page)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.id not in self._pages:
            return

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if reaction.id not in self._pages:
            return
