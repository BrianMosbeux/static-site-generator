import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType
from blocks_markdown import markdown_to_html_node


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
        self.assertEqual(block_to_block_type(heading), expected)

    def test_wrong_heading_3_tiny_title(self):
        heading = "#1"
        expected = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(heading), expected)

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

    def test_ordered_list_one_item_no_text(self):
        ordered = "1."
        expected = BlockType.PARAGRAPH
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

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
## Notes about C#
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Notes about C#</h2></div>"
        )

    def test_heading_with_formatting(self):
        md = """
### This is a heading with some **bold text** and some _italic text_.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading with some <b>bold text</b> and some <i>italic text</i>.</h3></div>"
        )

    def test_quote(self):
        md = """
> le poete est semblable au prince des nuees
>Qui hante la tempete et se rit de l'archer;
> Exilé sur le sol au milieu des huées,
>Ses ailes de géant l'empêche de marcher
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>le poete est semblable au prince des nuees Qui hante la tempete et se rit de l'archer; Exilé sur le sol au milieu des huées, Ses ailes de géant l'empêche de marcher</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- point one\n- point two"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>point one</li><li>point two</li></ul></div>"
        )
        pass

    def test_ordered_list(self):
        md = "1. point one\n2. point two\n3. point three\n4. point four\n5. point five\n6. point six\n7. point seven\n8. point height\n9. point nine\n10. point ten"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>point one</li><li>point two</li><li>point three</li><li>point four</li><li>point five</li><li>point six</li><li>point seven</li><li>point height</li><li>point nine</li><li>point ten</li></ol></div>"
        )


