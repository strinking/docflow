"""
This file contains various tests
for the cpp_symbol spider,
which is used to scrape documentation
for various C++ symbols (such as std::abs).
Although testing the Spider itself is
not directly possible, this file validates
various utility functions that are defined
in the file and used by the spider to
extract data such as the return values
of functions or the members of types.
"""

from urllib.request import urlopen

from docflow.scraper.spiders import cpp_symbol_spider


with urlopen("http://en.cppreference.com/w/cpp/numeric/math/abs") as ref:
    FUNC_ABS_HTML = ref.read()
FUNC_ABS_RETURN = "The absolute value of n (i.e. |n|), if it is representable."

with urlopen("http://en.cppreference.com/w/cpp/numeric/math/tan") as ref:
    FUNC_TAN_HTML = ref.read()
FUNC_TAN_RETURN = """If no errors occur, the tangent of arg (tan(arg)) is returned.
The result may have little or no significance if the magnitude of arg is large
(until C++11)
If a domain error occurs, an implementation-defined value is returned (NaN where supported)
If a range error occurs due to underflow, the correct result (after rounding) is returned."""


def test_clean_removes_tags():
    """
    Validates that clean() removes HTML tags.
    Internally, this is done through calling
    `unescape` from the w3lib library.
    """

    unclean = "<p>here is some markup</p>"
    cleaned = cpp_symbol_spider.clean(unclean, "")
    assert cleaned == "here is some markup"


def test_clean_replaces_unwanted():
    """
    Validates that clean() properly removes
    unwanted strings that are passed after
    the string that should be cleaned.
    """

    unclean = "this 8is unc1lean"
    cleaned = cpp_symbol_spider.clean(unclean, "8", "un", "1")
    assert cleaned == "this is clean"


def test_clean_unescape_html():
    """
    Validates that clean() properly
    unescapes HTML. For this, a string
    with HTML entities is passed.
    Read more here:
        https://www.w3schools.com/HTML/html_entities.asp
    """

    unclean = "3 &lt; 5, but 3 &gt; 1"
    cleaned = cpp_symbol_spider.clean(unclean, "")
    assert cleaned == "3 < 5, but 3 > 1"


def test_get_return_values():
    """
    Validates that the get_return_values
    scraper function properly extracts
    the return values for functions, and
    returns None where no return values
    or "garbage" was found.
    """

    abs_ret = cpp_symbol_spider.get_return_values(FUNC_ABS_HTML)
    assert abs_ret == FUNC_ABS_RETURN

    tan_ret = cpp_symbol_spider.get_return_values(FUNC_TAN_HTML)
    assert tan_ret == FUNC_TAN_RETURN
