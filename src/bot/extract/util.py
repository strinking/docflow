"""
Contains various utility-related functions
for the extraction package.
"""

import os


def get_ref_path(filename: str) -> str:
    """
    Returns the absolute path to the reference
    file specified by `filename`.
    """

    return os.path.join(
        os.path.abspath(os.path.pardir), "docflow", "data", filename
    )

