"""
This simply imports the start
function from the run script
which was originally used to start
the bot, but is now used inside
of __main__.py in order to be able
to start the bot as a module,
allowing relative imports and
other configuration options.
"""

from docflow.bot.run import start
