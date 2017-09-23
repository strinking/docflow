import asyncio
import datetime

import discord


CHARS_PER_PAGE = 1000
EMBED_EXPIRY = 5.0


class LongContentEmbed:
    """
    A class similiar to `PagedEmbed` that, when
    passed a long string, splits it up into
    multiple pages. It also enables users
    to navigate through it using reactions,
    similiar to how a PagedEmbed does it.
    """

    def __init__(self, content, title, colour, invoker_id):
        def create_base(page=1):
            return discord.Embed(
                title=title,
                timetamp=datetime.datetime.utcnow(),
                colour=colour
            ).set_footer(
                text=f"Page {page} / {len(self.pages)}",
            )
        self.create_base = create_base
        self.invoker_id = invoker_id
        self.msg = None
        self.position = 0
        self.pages = list(content[i:i + CHARS_PER_PAGE]
                          for i in range(0, len(content),
                                         CHARS_PER_PAGE))

    async def move_page_rel(self, move_by):
        """
        "Moves" the page by the specified
        amount, for example `1` to advance
        by one page or `-2` to move back
        two pages.
        """

        moved_pos = self.position + move_by
        if moved_pos < 0 or moved_pos > len(self.pages) - 1:
            return

        embed = self.create_base(moved_pos)
        embed.description = self.pages[moved_pos]
        await self.msg.edit(embed=embed)
        self.position = moved_pos

    async def on_reaction_add(self, reaction, user):
        """
        The event handler for the reaction_add
        event defined by discord.py. The
        PagedEmbed uses this to change its pages
        when appropriate. Additionally, when
        a user reacts with a reaction that
        causes this LongContentEmbed to change its
        contents, the bot will automatically
        remove the reaction to easily allow
        further navigation.
        You probably do not want to use this directly.
        """

        as_string = str(reaction)
        if user.bot:
            return

        if reaction.message.id == self.msg.id:
            if as_string == '⬅':
                await self.move_page_rel(-1)
            elif as_string == '➡':
                await self.move_page_rel(1)
            await self.msg.remove_reaction(reaction, user)

    async def send(self, ctx, bot):
        """
        Sends the Embed to the specified Context.
        The context is usually the place where
        a command using the LongContentEmbed
        was invoked.
        """

        embed = self.create_base()
        embed.description = self.pages[0]
        self.msg = await ctx.send(embed=embed)
        await self.msg.add_reaction('⬅')
        await self.msg.add_reaction('➡')
        bot.add_listener(self.on_reaction_add)

        await asyncio.sleep(60 * EMBED_EXPIRY)
        await self.msg.delete()
        bot.remove_listener(self.on_reaction_add)
