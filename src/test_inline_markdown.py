import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        res = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        self.assertEqual(new_nodes, res)

    def test_no_closing(self):
        node = TextNode("This is text with a `code block`` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_slit(self):
        node = TextNode("This is text with multiple **bold words** here is **another** and here is a **third**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        res = [
            TextNode("This is text with multiple ", TextType.TEXT, None),
            TextNode("bold words", TextType.BOLD, None),
            TextNode(" here is ", TextType.TEXT, None),
            TextNode("another", TextType.BOLD, None),
            TextNode(" and here is a ", TextType.TEXT, None),
            TextNode("third", TextType.BOLD, None),
        ]
        self.assertEqual(new_nodes, res)

    def test_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        res = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        self.assertEqual(new_nodes, res)

    def test_old_node_not_TEXT(self):
        node = TextNode("_This is text with a **bold** word_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        res = [TextNode("_This is text with a **bold** word_", TextType.ITALIC)]
        self.assertEqual(new_nodes, res)

    def test_multiple_old_nodes(self):
        node1 = TextNode("This is text with a **code block** word", TextType.TEXT)
        node2 = TextNode("This is text with multiple **bold words** here is **another** and here is a **third**", TextType.TEXT)
        node3 = TextNode("This is text with a **italic** word", TextType.TEXT)
        node4 = TextNode("_This is text with a **bold** word_", TextType.ITALIC)
        res1 = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.BOLD, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        res2 = [
            TextNode("This is text with multiple ", TextType.TEXT, None),
            TextNode("bold words", TextType.BOLD, None),
            TextNode(" here is ", TextType.TEXT, None),
            TextNode("another", TextType.BOLD, None),
            TextNode(" and here is a ", TextType.TEXT, None),
            TextNode("third", TextType.BOLD, None),
        ]
        res3 = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("italic", TextType.BOLD, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        res4 = [TextNode("_This is text with a **bold** word_", TextType.ITALIC)]
        new_nodes = split_nodes_delimiter([node1, node2, node3, node4], "**", TextType.BOLD)
        res = res1 + res2 + res3 + res4
        self.assertEqual(new_nodes, res)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
