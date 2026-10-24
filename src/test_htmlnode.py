import unittest
from htmlnode import HTMLNode
import htmlnode

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, None, None)")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_values(self):
        child_node1 = HTMLNode("h1", "Main Title")
        child_node2 = HTMLNode("p", "Our first paragrpah") 
        node = HTMLNode(tag="div", value=None, children=[child_node1, child_node2], props={"id": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [child_node1, child_node2])
        self.assertEqual(node.props, {"id": "main"})



if __name__ == "__main__":
    unittest.main()
