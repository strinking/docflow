"""
Contains a spider for scraping the
bold links found on
-   http://en.cppreference.com/w/cpp
These pages contain overviews about
different language features, such as
the utility library or threading:
-   http://en.cppreference.com/w/cpp/thread
-   http://en.cppreference.com/w/cpp/utility
"""

import scrapy

from ..util import get_paragraphs


class StubSpider(scrapy.Spider):
    """
    Scrapes reference from overview stubs, for example
    the overview page for the Algorithms Library:
        http://en.cppreference.com/w/cpp/algorithm
    Links are obtained through scraping the index page
    for C++, being http://en.cppreference.com/w/cpp, for
    links that are enclosed within <b> tags.
    """

    name = "cpp-stubs"
    start_urls = [
        "http://en.cppreference.com/w/cpp"
    ]

    def parse(self, response):
        """
        Invokes the callback self.parse_stub for every link en-
        closed within <b> tags that is found on the index page.
        """
        for link in set(response.css("b a::attr(href)").extract()):
            yield response.follow(link, callback=self.parse_stub)

    @staticmethod
    def parse_stub(response):
        """
        Parses a single stub into a dictionary.

        Format description:

        {
            "name":      The name of the page, for example "Containers library"
            "items":     The paragraphs found on the page,
                         stored in "header": "content" pairs.
            "headers":   The headers that are mentioned within this stub.
            "link":      A link to the referenced stub page.
        }
        """
        page_name = response.css("h1.firstHeading::text").extract_first()
        headers = response.css("tr.t-dsc-header code::text").extract()
        items = get_paragraphs(response)
        yield {
            "name": page_name,
            "items": items,
            "headers": list(set(headers)),
            "link": response.url
        }
