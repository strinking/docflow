import discord
from discord.ext import commands


class EmbedPage(discord.Embed):
    pass


class PagedEmbed:
    def __init__(self, ctx, bot: commands.Bot, idx_emoji, *args, **kwargs):
        self._ctx = ctx
        self._bot = bot
        self._msg = None

        # Dictionary to contain embed Pages in the following format:
        #   {
        #       "idx_emoji": EmbedPage,
        #       "emoji": EmbedPage,
        #       "emoji": EmbedPage,
        #       ...
        #   }
        self._pages = {
            idx_emoji: EmbedPage(*args, **kwargs)
        }
        self.current_page = self._pages[idx_emoji]

        # Attach our event listeners to the bot
        self._bot.add_listener(self.on_reaction_add)

    def add_page(self, emoji: str, page: EmbedPage):
        if emoji in self._pages:
            raise ValueError("An EmbedPage for this Emoji was already added")
        self._pages[emoji] = page

    async def send(self):
        self._msg = await self._ctx.send(embed=self.current_page)
        for reaction in self._pages:
            await self._msg.add_reaction(reaction)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        as_string = str(reaction)
        if reaction.message != self._msg or user == self._bot.user:
            return
        elif as_string not in self._pages:
            return
        await self._msg.edit(embed=self._pages[as_string])
        await self._msg.remove_reaction(reaction, user)

