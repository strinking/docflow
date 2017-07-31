"""
Contains a Spider for scraping data from the links
of the C++ symbol index, such as
-   http://en.cppreference.com/w/cpp/thread/thread
-   http://en.cppreference.com/w/cpp/container/vector
There are currently two different parsers for the
links that are parsed here, namely one for function
symbols, such as std::abs, and one for type symbols,
such as std::vector or std::thread (see above).
"""

from html import unescape
from typing import List, Optional

import scrapy
from w3lib.html import remove_tags

RETURN_VALUE_HEADER = b'<span class="mw-headline" id="Return_value">Return value</span>'

def clean(string: str, *remove: str):
    """
    removes HTML tags and unescapes HTML encoded strings and 
    optionally removes any specified strings from the resulting string
    """

    clean_str = unescape(remove_tags(string))
    for item in remove:
        clean_str = clean_str.replace(item, "")
    return clean_str


def get_description(member: str):
    """Returns the description of a member type or function extracted from a table on a symbol page"""

    split_member = member.split("\n\n")
    if len(split_member) > 1:
        return split_member[1].strip()
    return "No description available"


def get_title(member: str):
    """Returns the title of a member string extracted from a table on a symbol page"""

    return member.split("\n\n")[0].strip()


def get_from_table(filter_text: str, tables: List[str]):
    """
    Returns a dictionary containing information from a two column
    table which contains the filter_text in the form of Title : Description
    """

    for table in tables:
        if filter_text in table:
            members = clean(table).split("\n\n\n\n")
            member_titles = [get_title(member) for member in members]
            member_descriptions = [get_description(member) for member in members]
            return dict(zip(member_titles, member_descriptions))


def get_return_values(resp: str) -> Optional[str]:
    """
    Attempts to extract the return values
    from the response body. If this is longer
    than around 250 characters, chances are
    high that it's garbage, meaning that
    no return values were found.
    """

    start = resp.find(RETURN_VALUE_HEADER)
    if start is None:
        return None
    start += len(RETURN_VALUE_HEADER)
    end = resp.find(b"<h3>", start)
    ret_vals = unescape(remove_tags(resp[start:end]))
    return ret_vals if len(ret_vals) < 250 else None


def get_signatures(resp: scrapy.http.Response) -> str:
    """
    Placeholder function to return
    signatures of a symbol function.
    """

    signatures = resp.css(
        "tbody tr.t-dcl"
    ).extract()
    return remove_tags(
        unescape(
            ''.join(s.replace('\u00a0', '') for s in signatures)
        )
    ).strip()


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

    def parse(self, response: scrapy.http.Response):
        """
        Invokes the callback self.parse_symbol_index
        for every link found on this page. A certain
        relevance is already validated here.
        """

        for url in set(response.css('a::attr(href)').extract()):
            if url.startswith("/w/cpp") and not url.endswith('symbol_index'):
                yield response.follow(url, callback=self.parse_symbol_index)

    def parse_symbol_index(self, resp: scrapy.http.Response):
        """
        Parses a single symbol found
        in the std:: namespace.
        """

        names = resp.css("h1.firstHeading::text").extract()
        if not all((n.islower() or n == '_' and n.startswith("std::")) for n in names):
            # It's some unwanted link, ignore it
            return
        elif get_return_values(resp.body) is not None:
            # It's a function, yield from the function symbol parser
            yield from self.parse_function(resp)
        else:
            # It's a type, yield from the type symbol parser
            yield from self.parse_type(resp)

    @staticmethod
    def parse_function(resp: scrapy.http.Response):
        """
        Parses a function symbol.

        Examples:
            http://en.cppreference.com/w/cpp/numeric/complex/abs
            http://en.cppreference.com/w/cpp/algorithm/accumulate
            http://en.cppreference.com/w/cpp/io/manip/hex
        """

        names = resp.css("h1.firstHeading::text").extract()
        names_without_commas = [
            n.replace(', ', '') for n in names if n != ', '
        ]
        if not names_without_commas:
            return
        elif not all(n.islower() or n == '_' for n in names_without_commas):
            return

        headers = resp.css(
            "tr.t-dsc-header a::text"
        ).extract()
        signatures = get_signatures(resp)
        description = resp.css(
            "div.mw-content-ltr"
        ).xpath("string(p)").extract()
        return_values = get_return_values(resp.body)
        parameters = resp.css(
            "table.t-par-begin"
        ).xpath("string(.//tr)").extract()
        example = resp.css(
            "div.t-example div.cpp"
        ).xpath("string(pre)").extract_first()

        yield {
            'type': 0,
            'names': [
                "std::" + n for n in names_without_commas
            ],
            'header': list(set(headers)),
            'sigs': signatures,
            'desc': [
                remove_tags(paragraph) for paragraph in description
            ],
            'return': return_values,
            'params': [
                param.replace('\n', '').strip() for param in parameters
            ],
            'example': example,
            'link': resp.url
        }

    @staticmethod
    def parse_type(resp: scrapy.http.Response):
        """
        Parses a type symbol.

        Examples:
            http://en.cppreference.com/w/cpp/thread/thread
            http://en.cppreference.com/w/cpp/container/vector
        """

        name = resp.css("h1.firstHeading::text").extract_first()
        if name is None:
            return
        header = resp.css("tr.t-dsc-header a::text").extract()
        sigs = get_signatures(resp)
        desc = resp.css("div.mw-content-ltr").xpath("string(p)").extract()
        tables = resp.css("table.t-dsc-begin").extract()
        types = get_from_table("Member type", tables)
        funcs = get_from_table("member function", tables)

        yield {
            'type': 1,
            'names': ["std::" + name],
            'header': header,
            'sigs': sigs,
            'desc': desc,
            'types': types,
            'funcs': funcs,
            'link': resp.url
        }
