"""
This File tests whether python files found in `src` and `test` are conform
to style guides such as PEP8 using pycodestyle.
"""
import os
import unittest
import subprocess


FAIL_MSG = 'Found a total of {} code style errors (and warnings), use ' \
           '`pylint test/` and `pylint src/` to read about them in detail.'


def get_py_files(dirname: str):
    """Gets the paths to all .py files found in the specified directory"""
    files = []
    for _, _, directory_files in os.walk(dirname):
        for file_name in directory_files:
            if file_name.endswith('.py'):
                files.append(os.path.join(dirname, file_name))
    return files


class TestCodeFormat(unittest.TestCase):
    """Class containing a test for the PEP8 Style on Python source files."""

    def test_pep8(self):
        """Test that all source files are conform to PEP8."""
        for file in get_py_files('src') + get_py_files('test'):
            with subprocess.Popen(['pylint', file],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL) as result:
                decoded = [
                    line.decode('utf-8') for line in result.stdout.readlines()
                    if line != b'' and line[0] in b'WCRFE'
                ]
            self.assertTrue(not decoded, \
                        f'{FAIL_MSG.format(len(decoded))}\n\nIn {file}:\n{"".join(decoded)}')


if __name__ == '__main__':
    unittest.main()
