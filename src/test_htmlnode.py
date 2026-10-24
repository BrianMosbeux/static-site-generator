import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link", props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">link</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_with_children(self):
        with self.assertRaises(TypeError):
            node = LeafNode(None, value="hello", children=["a", "b"])

    def test_leaf_empty(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

    def test_leaf_tag_none(self):
        node = LeafNode(None, "Hi there")
        self.assertEqual(repr(node), "LeafNode(None, Hi there, None)")

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
        
class TestParentNode(unittest.TestCase):
    def test_missing_tag(self):
        with self.assertRaises(TypeError):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(children=[child_node])

    def test_missing_children(self):
        with self.assertRaises(TypeError):
            parent_node = ParentNode("p")

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    

if __name__ == "__main__":
    unittest.main()
