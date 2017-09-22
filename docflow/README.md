# `bot` subdirectory
This directory contains the source code
for the Discord Bot itself.

The files in here (apart from `__init__.py` 
and `run.py`) are command groups (Cogs)
which are loaded on startup and can be loaded and
unloaded at runtime through commands as needed.
Note, however, that unloading the `Admin` cog
will result in not being able to load or unload
any more cogs, since this cog contains the
commands necessary to do so.

The subdirectory `extract` handles extracting the
scraped documentation and creating Embeds out of
them which can then be easily sent through Discord.
The commands to search & extract documentation data
for various languages are found in `doc.py`.

The subdirectory `util` currently only houses
the code evaluation cog for using 
[Coliru](http://coliru.stacked-crooked.com).
This runs asynchronous to not block the bot's
event loop.

