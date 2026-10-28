import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_trailing_white_space(self):
        md = """
    This is **bolded** paragraph     

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line          

                 - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



class TestBlockToBlockQuote(unittest.TestCase):
    def test_heading(self):
        heading = "## This is a h2 heading"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(heading), expected)

    def test_heading_6(self):
        heading = "###### This is a h2 heading"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(heading), expected)

    def test_heading_tiny_title(self):
        heading = "# 1"
        expected = BlockType.HEADING
        self.assertEqual(block_to_block_type(heading), expected)

    def test_empty_string(self):
        heading = ""
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(heading), expected)

    def test_wrong_heading_1(self):
        heading = "#This hading is lacking space after #"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(heading), expected)
        
    def test_wrong_heading_2(self):
        heading = "####### h7 does not exists dummy"
        expected = BlockType.PARAGRAPH

    def test_wrong_heading_3_tiny_title(self):
        heading = "#1"
        expected = BlockType.PARAGRAPH

    def test_code(self):
        code = "```\nthis is som code block\n```"
        expected = BlockType.CODE
        self.assertEqual(block_to_block_type(code), expected)

    def test_code_empty_no_newline(self):
        code = "``````"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(code), expected)

    def test_code_too_short(self):
        code = "`````"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(code), expected)

    def test_code_too_short_2(self):
        code = "```"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(code), expected)

    def test_quote(self):
        quote = ">quoting\n> quoting too\n> just another for fun"
        expected = BlockType.QUOTE
        self.assertEqual(block_to_block_type(quote), expected)

    def test_unordered_list(self):
        unordered = "- point one\n- point two"
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(block_to_block_type(unordered), expected)

    def test_wrong_unordered(self):
        unordered = "-point one\n-point two"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(unordered), expected)

    def test_ordered_list(self):
        ordered = "1. point one\n2. point two"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(ordered), expected)

    def test_wrong_ordered_list_nonincremental(self):
        ordered = "1. point one\n2. point two\n7. point seven\n4. point four"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(ordered), expected)

    def test_wong_ordered_list_missing_dot(self):
        ordered = "1. point one\n2. point two\n3 point three"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(ordered), expected)

    def test_wong_ordered_list_missing_white_space(self):
        ordered = "1. point one\n2. point two\n3.point three"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(ordered), expected)

        
    def test_wong_ordered_list_too_short(self):
        ordered = "1. point one\n2. point two\n3"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(ordered), expected)

        
    def test_ordered_double_digits(self):
        ordered = "1. point one\n2. point two\n3. point three\n4. point four\n5. point five\n6. point six\n7. point seven\n8. point height\n9. point nine\n10. point ten"
        expected = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(ordered), expected)



