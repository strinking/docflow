"""
This File tests whether python files found in `src` and `test` are conform
to style guides such as PEP8 using pycodestyle.
"""
import os
import unittest

import pycodestyle


FAIL_MSG = 'Found a total of {} code style errors (and warnings), use ' \
           '`pylint test/` and `pylint src/` to read about them in detail.'


def get_py_files(dirname: str):
    """Gets the paths to all .py files found in the specified directory"""
    files = []
    for _, _, directory_name in os.walk(dirname):
        for file_name in directory_name:
            if file_name.endswith('.py'):
                files.append(file_name)
    return files


class TestCodeFormat(unittest.TestCase):
    """Class containing a test for the PEP8 Style on Python source files."""

    def test_pep8(self):
        """Test that all source files are conform to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(get_py_files('src') + get_py_files('test'))
        self.assertEqual(result.total_errors, 0,
                         FAIL_MSG.format(result.total_errors))


if __name__ == '__main__':
    unittest.main()
