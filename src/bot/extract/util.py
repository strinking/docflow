"""
Contains various utility-related functions
for the extraction package.
"""

import os
import json


def get_ref_path(filename: str) -> str:
    """
    Returns the absolute path to the reference
    file specified by `filename`.
    """

    return os.path.join(
        os.path.abspath(os.path.pardir), "docflow", "data", filename
    )


def get_ref(filename: str) -> dict:
    """
    Returns the parsed contents of a reference file
    to be kept in memory for faster access.
    """

    with open(get_ref_path(filename), 'r') as f:
        return json.load(f)
