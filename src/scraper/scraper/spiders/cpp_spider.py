import scrapy


class BjarneSpider(scrapy.Spider):
    name = "cppreference"
    start_urls = [
        "http://en.cppreference.com/w/c",
        "http://en.cppreference.com/w/cpp"
    ]

    # Parse the index websites listed above
    def parse(self, response):
        for url in response.css('a::attr(href)'):
            # http://en.cppreference.com/w/cpp/language - overview page about language constructs
            if url.endswith('language'):
                pass
            # http://en.cppreference.com/w/cpp/symbol_index - list of all symbols in the std namespace
            elif url.endswith('symbol_index'):
                yield response.follow(url, callback=self.parse_symbol_index)
            # generic language-related pages, for example http://en.cppreference.com/w/cpp/algorithm
            elif url.startswith('/w/c'):
                # yield response.follow(base_url + url, callback=)
                pass
