"""
Converts all HTML files in the `data`
directory to Discord-friendly Markdown.
"""

import glob
import os

from markdownify import markdownify


if __name__ == '__main__':
    for fname in glob.iglob("data/**/*.html"):
        with open(fname) as f:
            html = f.read()
        with open(fname.split('.')[0] + '.md', 'w+') as f:
            f.write(markdownify(html))
        os.remove(fname)
