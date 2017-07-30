from html import unescape

import scrapy
from w3lib.html import remove_tags

RETURN_VALUE_HEADER = b'<span class="mw-headline" id="Return_value">Return value</span>'


def get_return_values(resp: str) -> str:
    """
    Attempts to extract the return values
    from the response body. If this is longer
    than around 80 characters, chances are
    high that it's garbage, meaning that
    no return values were found.
    """

    start = resp.find(RETURN_VALUE_HEADER)
    if start is None:
        return None
    start += len(RETURN_VALUE_HEADER)
    end = resp.find(b"<h3>", start)
    return unescape(remove_tags(resp[start:end]))



def get_signatures(resp: str) -> str:
    pass


class CppSymbolSpider(scrapy.Spider):
    """
    Scrapes reference from the C++ symbol index:
    http://en.cppreference.com/w/cpp/symbol_index
    Basically this scrapes all symbols found in the
    std:: namespace. Several checks are done to
    ensure that only actual symbols are scraped.
    """

    name = "cpp-symbols"
    start_urls = [
        "http://en.cppreference.com/w/cpp/symbol_index"
    ]

    def parse(self, response):
        """
        Invokes the callback self.parse_symbol_index
        for every link found on this page. A certain
        relevance is already validated here.
        """

        for url in set(response.css('a::attr(href)').extract()):
            if url.startswith("/w/cpp") and not url.endswith('symbol_index'):
                yield response.follow(url, callback=self.parse_symbol_index)

    @staticmethod
    def parse_symbol_index(response):
        """
        Parses a single symbol found
        in the std:: namespace.
        """

        names = response.css("h1.firstHeading::text").extract()
        names_without_commas = [
            n.replace(', ', '') for n in names if n != ', '
        ]
        if not names_without_commas:
            return
        elif not all(
                n.islower() or n == '_' for n in names_without_commas
        ):
            return

        headers = response.css(
            "tr.t-dsc-header a::text"
        ).extract()
        signatures = response.css(
            "tbody tr.t-dcl span::text"
        ).extract()
        description = response.css(
            "div.mw-content-ltr"
        ).xpath("string(p)").extract()
        parameters = response.css(
            "table.t-par-begin"
        ).xpath("string(.//tr)").extract()
        return_values = get_return_values(response.body)
        example = response.css(
            "div.t-example div.cpp"
        ).xpath("string(pre)").extract_first()

        yield {
            'names': [
                "std::" + n for n in names_without_commas
            ],
            'defined_in_header': list(set(headers)),
            'sigs': ''.join(
                s.replace('\u00a0', '') for s in signatures
            ).split(';'),
            'desc': [
                remove_tags(paragraph) for paragraph in description
            ],
            'return': return_values,
            'params': [
                param.replace('\n', '').strip() for param in parameters
            ],
            'example': example,
            'link': response.url
        }
