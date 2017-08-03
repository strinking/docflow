"""
This module defines two classes
for creating so-called paged Embeds.

Paged Embeds are a special type of
message through which other Users
can navigate through Reactions.
The content of each "page" is
an Embed, effectively allowing the
developer to contain 20 embeds
in a single message.

By default, paged Embeds stop
responding to reactions after
5 minutes. This interval can be
changed through the variable
    EMBED_EXPIRY
, which sets the interval for
an embed to "expire", in minutes.
This is achieved through using
    threading.Timer
, which is started when
the message is sent.
"""

from threading import Timer

import discord
from discord.ext import commands

# After how many minutes the PagedEmbed should ignore reactions
EMBED_EXPIRY = 5.0


class EmbedPage(discord.Embed):
    """
    A subclass of discord.Embed
    which represents a single
    page of content in a PagedEmbed.
    """


class PagedEmbed:
    """
    A custom type that implements
    a collection of EmbedPages which
    are navigatable through reactions.

    The PagedEmbed will attach an
    event listener for the reaction
    add event which it uses to edit
    its content independently without
    having to override the default
    on_reaction_add method from the
    client. To avoid infinitely
    cluttering up the handlers for the
    reaction add event, sending the
    PagedEmbed will start a
    threading.Timer which automatically
    deattaches the event handler from
    the bot after the interval set in
    the variable EMBED_EXPIRY, in minutes.
    This defaults to removing the handler
    after five minutes, but simply
    assigning another value to the
    variable will change this behavior

    for all PagedEmbeds that are sent
    after it was changed.

    Please note that the bot requires
    a set of permissions for the
    PagedEmbed to work properly:
    - Sending Messages
        Should be fairly obvious why.
    - Adding Reactions
        For showing the users which
        reactions result in "browsing"
        different pages in the message.
    - Manage Messages
        For removing reactions after
        users added them to navigate
        the PagedEmbed.
    - (Use External Emojis)
        Optional, if you want to use
        external emojis for the embed
        pages (the Bot needs this
        permission in order to be able
        to react with the external
        emojis you pass to add_page).

    It is currently only possible to
    use this with discord.py's commands
    extension as it requires the
    `add_listener` method which the
    regular discord.Client class does
    not implement.

    Example:

        # Inside your Cog...
        @commands.command()
        async def colours(self, ctx):
            embed = PagedEmbed(ctx, bot, "🍏",
                title="Green!",
                description="An apple a day keeps the code debt away.",
                colour=discord.Colour.green()
            )
            embed.add_page("💛", EmbedPage(
                title="Yellow!",
                description="I don't know what to put here.",
                colour=discord.Colour.gold()
            ))
            embed.add_page("🚗", EmbedPage(
                title="Red!",
                description="A red car. That's it!",
                colour=discord.Colour.red()
            ))
            await embed.send()
    """

    def __init__(self, ctx, bot: commands.Bot, idx_emoji, *args, **kwargs):
        """
        Create a new PagedEmbed.

        Arguments:
            ctx : discord.ext.commands.Context
                The context in which the command
                to send the PagedEmbed was invoked.
            bot : discord.ext.commands.Bot
                The bot that the application is
                logged in with. In Cogs, this is
                usually saved as an instance
                attribute `bot`.
            idx_emoji : str
                The Emoji which is used to navigate
                to the initial page, constructed
                through arguments and keyword
                arguments passed to this constructor.

        Example:
            embed = PagedEmbed(ctx, bot, "🍏",
                title="Index Page",
                description="This page gets shown initially."
            )
            embed.add_page("👍", EmbedPage(
                title="Second Page",
                description="This page gets shown when you click the 👍 emoji."
            ))
        """

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

    def detach_listener(self):
        """
        Detaches the event listener for the
        on_reaction_add event which the
        PagedEmbed uses to edit itself on a
        relevant reaction. Normally, you do
        not have to call this function
        manually, it is called automatically
        after a delay (see documentation for
        this class itself.).
        """

        self._bot.remove_listener(self.on_reaction_add)

    def add_page(self, emoji: str, page: EmbedPage):
        r"""
        Adds a page to this PagedEmbed.

        Arguments:
            emoji : str
                A Unicode Emoji like 👍 or 😃, or
                the full "text" of a discord Emoji
                which you can obtain by prepending
                a \ to the front of a Discord Emoji,
                resulting in something like this:
                <:FeelsWOAWMan:273546398996234242>
                Note, however, that the bot must be
                able to use the reaction. Since
                bots have access to Emojis as if
                they have Nitro, all valid emojis
                are stored in discord.Client.emojis.
            page : EmbedPage
                The EmbedPage which should be
                displayed when the given Emoji
                is reacted with / clicked.
        """

        if emoji in self._pages:
            raise ValueError("A handler or an EmbedPage for this Emoji was already added")
        self._pages[emoji] = page

    def add_handler(self, emoji: str, handler: callable):
        r"""
        Adds a handler for the given Emoji.

        This allows the bot to perform an
        operation in a function that is
        passed as `callable` when Discord
        users react with the given Emoji.

        The handler can be a coroutine or
        a regular function.

        Arguments:
            emoji : str
                A Unicode Emoji like 👍 or 😃, or
                the full "text" of a discord Emoji
                which you can obtain by prepending
                a \ to the front of a Discord Emoji,
                resulting in something like this:
                <:FeelsWOAWMan:273546398996234242>
                Note, however, that the bot must be
                able to use the reaction. Since
                bots have access to Emojis as if
                they have Nitro, all valid emojis
            handler : callable
                A function (either "regular" or a
                coroutine) that should be called
                when a user reacts with the emoji.
        """

        if emoji in self._pages:
            raise ValueError("A handler or an EmbedPage for this Emoji was already added")
        self._pages[emoji] = handler

    async def on_reaction_add(self, reaction, user):
        """
        The event handler for the reaction_add
        event defined by discord.py. The
        PagedEmbed uses this to change its pages
        when appropriate. Additionally, when
        a user reacts with a reaction that
        causes this PagedEmbed to change its
        contents, the bot will automatically
        remove the reaction to easily allow
        further navigation.
        You probably do not want to use this directly.
        """

        as_string = str(reaction)

        if user == self._bot.user or as_string not in self._pages:
            return
        elif reaction.message.id == self._msg.id:
            await self._msg.remove_reaction(reaction, user)
            handler = self._pages[as_string]

            if isinstance(handler, callable):
                await reaction()
            elif isinstance(handler, PagedEmbed):
                await self._msg.edit(embed=self._pages[as_string])

    async def send(self):
        """
        Sends the PagedEmbed to the context
        which was passed to the constructor.
        The bot will then add reactions to
        the sent message to show the users
        the navigation choices.
        """

        self._msg = await self._ctx.send(embed=self.current_page)

        for reaction in self._pages:
            await self._msg.add_reaction(reaction)

        # Start a timer to detach the event listener after the set interval
        Timer(EMBED_EXPIRY * 60, self.detach_listener).start()

    async def delete(self):
        """
        A shortcut to delete the underlying
        message of the PagedEmbed. By
        default, it is never deleted, only
        the "reaction add" event handler is
        detached after a set interval.
        """

        await self._msg.delete()
