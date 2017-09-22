"""
The entry point for the Bot
which will scrape data as needed.
You can start the bot by using
    python3 -m docflow.

Make sure to export an environment variable named
    DISCORD_TOKEN
set to your Discord token.

Command group / extension loading is not done
in this file. If you wish to add a new command
group to the bot at startup, please check out
    docflow/bot/run.py
instead. The file also contains various initial
setup configuration, such as setting the prefix,
the description along with basic event handlers.
"""

import os

from .run import start


REFERENCE_DIR = os.path.join(
    os.path.abspath(os.path.pardir), "docflow", "data"
)


if __name__ == '__main__':
    start()
