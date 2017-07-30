

# Command for the initial run of the bot, scrapes Documentation and then starts.
firstrun:
	echo "Scraping documentation data..."
	scrape
	echo "Installing requirements..."
	python3 -m pip install -r requirements.txt
	echo "Starting Bot..."
	python3 src/bot/run.py

# Simple shortcut for starting the bot.
run: 
	python3 src/bot/run.py

# Run all scraping spiders and put their results into the data/ directory
scrape:
	mkdir -p data/
	rm -rf data/*
	cd src/ && \
	scrapy crawl cpp-symbols --loglevel INFO -o ../data/cpp_symbols.json && \
	scrapy crawl cpp-stubs   --loglevel INFO -o ../data/cpp_stubs.json
