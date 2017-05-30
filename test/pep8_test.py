import os
import subprocess
import pycodestyle
import unittest


FAIL_MSG = 'Found a total of {} code style errors (and warnings), use ' \
           '`pylint test/` and `pylint src/` to read about them in detail.'

def get_py_files(dirname: str):
    """Gets the paths to all .py files found in the specified directory"""
    files = []
    for root, sub_folders, directory_name in os.walk(dirname):
        for file_name in directory_name:
            # Don't check the virtual environment
            if directory_name == 'venv':
                continue
            elif file_name.endswith('.py'):
                files.append(file_name)
    return files


class TestCodeFormat(unittest.TestCase):
    def test_pep8(self):
        """Test that all source files are conform to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(get_py_files('src') + get_py_files('test'))
        self.assertEqual(result.total_errors, 0, FAIL_MSG.format(result.total_errors))




if __name__ == '__main__':
    unittest.main()
