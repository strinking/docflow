"""Contains utility functions for spiders."""

import scrapy
from w3lib.html import remove_tags


def get_paragraphs(resp: scrapy.http.Response) -> dict:
    """
    Extracts headers and their respective paragraphs
    out of the response that is passed to this function.

    The headers and their paragraphs' contents are
    returned as a dictionary in the following format:

    {
        "Header": ["my", "content", "here"]
    }

    This makes it easy to obtain data from specific parts of
    a reference page, for example the arguments to a function.
    """

    headlines = (
        h for h in resp.css("span.mw-headline::text").extract() if h[0] != ' '
    )
    descriptions = (
        remove_tags(d) for d in resp.css("div.mw-content-ltr p").extract()
    )

    return dict(zip(headlines, descriptions))
