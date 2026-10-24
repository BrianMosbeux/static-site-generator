import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
