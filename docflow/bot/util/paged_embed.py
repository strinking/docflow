from threading import Timer

import discord
from discord.ext import commands


# After how many minutes the PagedEmbed should ignore reactions
EMBED_EXPIRY = 5.0


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

        # Attach our event listener to the bot
        self._bot.add_listener(self.on_reaction_add)

        # Detach the event listener after the set interval
        Timer(EMBED_EXPIRY * 60, self.detach_listener).start()

    def detach_listener(self):
        self._bot.remove_listener(self.on_reaction_add)

    def add_page(self, emoji: str, page: EmbedPage):
        if emoji in self._pages:
            raise ValueError("An EmbedPage for this Emoji was already added")
        self._pages[emoji] = page

    async def on_reaction_add(self, reaction, user):
        as_string = str(reaction)
        if user == self._bot.user or as_string not in self._pages:
            return
        elif reaction.message.id == self._msg.id:
            await self._msg.edit(embed=self._pages[as_string])
            await self._msg.remove_reaction(reaction, user)

    async def send(self):
        self._msg = await self._ctx.send(embed=self.current_page)
        for reaction in self._pages:
            await self._msg.add_reaction(reaction)

    async def delete(self):
        await self._msg.delete()

