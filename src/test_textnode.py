import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
        self.assertEqual(node.__repr__(), "TextNode(This is some anchor text, link, https://boot.dev)")

    def test_url_none(self):
        node = TextNode("This is an empty link", TextType.LINK, None)
        node2 = TextNode("This is an empty link", TextType.LINK)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("confirm italic != bold", TextType.BOLD)
        node2 = TextNode("confirm italic != bold", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a url node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a url node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_link_no_url(self):
        node = TextNode("This is a url node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a url node")
        self.assertEqual(html_node.props, {"href": None})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "This is an image node"})


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
