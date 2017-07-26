import scrapy
from w3lib.html import remove_tags

class StubSpider(scrapy.Spider):
    name = "stubs"
    start_urls = [
        "http://en.cppreference.com/w/cpp"
    ]

    def parse(self, response):
        for link in set(response.css("b a::attr(href)").extract()):
            yield response.follow(link, callback=self.parse_stub)

    @staticmethod
    def parse_stub(response):
        page_name = response.css("h1.firstHeading::text").extract_first()
        item_names = [headline for headline in response.css("span.mw-headline::text").extract() if headline[0] is not ' ']
        headers = response.css("tr.t-dsc-header code::text").extract()
        descriptions = [remove_tags(desc) for desc in response.css("div.mw-content-ltr p").extract()]
        yield {
            "name" : page_name,
            "items" : dict(zip(item_names, descriptions)),
            "defined_in_header" : list(set(headers)),
            "link" : response.url
        }
