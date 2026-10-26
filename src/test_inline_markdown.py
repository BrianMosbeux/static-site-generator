import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

class TextExtractMarkdownLinks(unittest.TestCase):
    def test_extract_urls(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

    def test_extract_urls_ignores_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and an image we want to ignore ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        matches = extract_markdown_links(text)
        self.assertListEqual(expected, matches)

if __name__ == "__main__":
    unittest.main()
