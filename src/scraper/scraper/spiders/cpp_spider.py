import scrapy
from w3lib.html import remove_tags


class BjarneSpider(scrapy.Spider):
    name = "cppreference"
    # Use google webcache instead?
    # http://webcache.googleusercontent.com/search?q=cache:en.cppreference.com/w/c/
    start_urls = [
        "http://en.cppreference.com/w/c",
        "http://en.cppreference.com/w/cpp"
    ]

    # Parse the index websites listed above
    def parse(self, response):
        for url in response.css('a::attr(href)').extract():
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

    # Parses the C++ Symbol Index http://en.cppreference.com/w/cpp/symbol_index
    def parse_symbol_index(self, response):
        for url in response.css('p a::attr(href)'):
            # print(url)
            yield response.follow(url, callback=self.parse_std_symbol)

    # Parses an C++ symbol defined in the standard namespace, from the index above
    @staticmethod
    def parse_std_symbol(response):
        names = response.css("h1.firstHeading::text").extract()
        headers = response.css("tr.t-dsc-header a::text").extract()
        signatures = response.css("tbody tr.t-dcl span::text").extract()
        description = response.css("div.mw-content-ltr").xpath("string(p)").extract()
        parameters = response.css("table.t-par-begin").xpath("string(.//tr)").extract()
        return_values = response.css("div.mw-content-ltr > div.t-li1").extract()
        example = response.css("div.t-example div.cpp").xpath("string(pre)").extract_first()
        yield {
            'names': [
                "std::" + x.replace(', ', '') for x in names if x != ', '
            ],
            'defined_in_header': list(set(headers)),
            'sigs': ''.join(signatures).split(';'),
            'desc': [
                remove_tags(paragraph) for paragraph in description
            ],
            'return': [
                remove_tags(r_val) for r_val in return_values
            ],
            'params': [
                param.replace('\n', '') for param in parameters
            ],
            'example': example
        }
