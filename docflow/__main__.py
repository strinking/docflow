"""
The entry point for the Bot
which will scrape data as needed.
You can start this script by using
    python3 -m docflow
If no reference files for the documentation
search exist, this entry point will attempt
to download them through scrapy automatically.

If you wish to scrape the files manually,
simply pass `scrape` as an argument:
    python3 -m docflow scrape
This will start the also start the bot afterwards.
Make sure to export an environment variable named
    DISCORD_TOKEN
since the bot uses this to securely log in
without the need to store the token somewhere
in plain text or other configuration files
that one could push to version control by accident.

Command group / extension loading is not done
in this file. If you wish to add a new command
group to the bot at startup, please check out
    docflow/bot/run.py
instead. The file also contains various initial
setup configuration, such as setting the prefix,
the description along with basic event handlers.
"""

import os
import subprocess
import sys

from . import start

SCRAPY_SPIDERS = (
    "cpp_stubs",
    "cpp_symbols"
)

SCRAPY_DIR = os.path.join(
    os.path.abspath(os.path.pardir), "docflow", "docflow", "scraper"
)

REFERENCE_DIR = os.path.join(
    os.path.abspath(os.path.pardir), "docflow", "data"
)

INITIAL_DIR = os.getcwd()


def run_spider(spider_name: str):
    """
    Runs a single spider and outputs
    to a JSON file. Log levels are
    set to WARN to reduce clutter.
    """

    spider_file_name = spider_name.lower() + ".json"
    spider_path = os.path.join(REFERENCE_DIR, spider_file_name)

    if os.path.exists(spider_path):
        os.remove(spider_path)
        print(f"Removed existing reference file {spider_file_name}.")

    subprocess.Popen(
        [
            "python3", "-m",
            "scrapy", "crawl", spider_name,
            "--loglevel", "WARN",
            "-o", spider_path
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    ).communicate()


def scrape_data():
    """
    Runs all spiders specified above
    and informs the user about the start
    and end of each spider.
    """

    print("Changing to scrapy directory...")
    os.chdir(SCRAPY_DIR)

    for spider in SCRAPY_SPIDERS:
        print(f"Running Spider {spider}... ")
        run_spider(spider)
        print("Done.")
    print("Scraping done. Changing back to initial directory.")
    os.chdir(INITIAL_DIR)


if __name__ == '__main__':
    print("Checking if reference files exist...")

    os.makedirs(REFERENCE_DIR, exist_ok=True)

    if not os.listdir(REFERENCE_DIR):
        print("Reference files do not exist. Starting Scrapy...")
        scrape_data()
    elif sys.argv.pop() == "scrape":
        print("Scraping was manually invoked. Starting Scrapy...")
        scrape_data()
    else:
        print("References files found.")

    print("Starting the Bot through run.py...")
    start()
