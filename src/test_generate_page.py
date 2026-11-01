import unittest
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_oneline_markdown(self):
        title = extract_title("# Hello")
        self.assertEqual(title, "Hello")

    def test_no_title_markdown(self):
        with self.assertRaises(ValueError):
            extract_title("### Hello")

    def test_long_markdown(self):
        markdown = """
# This is our title

Then we have some kind of summary

## Then a secondary h2 title

Some text

- an item
- another item

### An h3 

and some whathever lorem ipsum stuff. Excpect I do not speal latin
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is our title")


    

