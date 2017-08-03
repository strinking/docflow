# Main package
This package marks the entry point for docflow.
Everything written in `__main__.py` modifies the startup
process when the bot is started using `python3 -m docflow`.

The two subdirectories `bot` and `scraper` are for the Discord
Bot and the documentation scraper, respectively.

After the scraper ran at least once, a directory named `.scrapy`
will also appear (ignored by Git). Scrapy uses this to cache
files from past scraping runs, resulting in a lot faster subsequent
scraping runs.
