from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other) -> bool:
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}) 
        case _:
            raise ValueError(f"invalid text type {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
        elif delimiter in n.text:
            splitted_text = n.text.split(delimiter)
            if len(splitted_text) % 2 != 1:
                raise Exception("Error: Invalid markdown syntax, one of the delimiter has not been closed")
            splitted_nodes = []
            for j, m in enumerate(splitted_text):
                if m == "":
                    continue
                if j % 2 == 0:
                    splitted_nodes.append(TextNode(m, n.text_type))
                else:
                    splitted_nodes.append(TextNode(m, text_type))
            new_nodes.extend(splitted_nodes)
        else:
            new_nodes.append(n)
    return new_nodes

            
            


