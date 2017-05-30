import os
import pycodestyle
import unittest

class TestCodeFormat(unittest.TestCase):
    def get_source_file_names(self):
        """Gets the paths to all .py files found in the `src` directory"""
        files = []
        for root, sub_folders, files in os.walk('src'):
            for file in files:
                if file.endswith('.py'):
                    files.append(file)
        return files

    def test_pep8(self):
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(self.get_source_file_names())
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
