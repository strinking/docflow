

# Run all scraping spiders and put their results into the doc/ directory
scrape:
	mkdir -p doc/
	rm -rf doc/*
	cd src/ && \
	scrapy crawl cpp-symbols -o ../doc/cpp_symbols.json && \
	scrapy crawl cpp-stubs -o ../doc/cpp_stubs.json
