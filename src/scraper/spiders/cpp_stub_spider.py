import scrapy
from w3lib.html import remove_tags


from ..util import get_paragraphs


class StubSpider(scrapy.Spider):
    name = "cpp-stubs"
    start_urls = [
        "http://en.cppreference.com/w/cpp"
    ]

    def parse(self, response):
        for link in set(response.css("b a::attr(href)").extract()):
            yield response.follow(link, callback=self.parse_stub)

    @staticmethod
    def parse_stub(response):
        page_name = response.css("h1.firstHeading::text").extract_first()
        headers = response.css("tr.t-dsc-header code::text").extract()
        descriptions = [
            remove_tags(desc) for desc in response.css("div.mw-content-ltr p").extract()
        ]
        yield {
            "name" : page_name,
            "items" : get_paragraphs(response),
            "items_raw" : descriptions,
            "defined_in_header" : list(set(headers)),
            "link" : response.url
        }
