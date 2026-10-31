from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextType, text_node_to_html_node, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"   


class BlockNode:
    def __init__(self, tag: str, block_type: BlockType, children: list[HTMLNode]):
        self.tag = tag
        self.block_type = block_type
        self.children = children

    def __repr__(self):
        return f"BlockNode({self.block_type}, {self.children})"


def markdown_to_blocks(markdown: str) -> list[str]:
    splitted_markdown = markdown.split("\n\n")
    stripped_markdown = [s.strip() for s in splitted_markdown if s.strip() != ""]
    return stripped_markdown

def block_to_block_type(block: str) -> BlockType:
    if block == "":
        return BlockType.PARAGRAPH
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    splitted_lines = block.split("\n")
    filter_quote = list(filter(lambda x: x.startswith(">"), splitted_lines))
    filter_unordered_list = list(filter(lambda x: x.startswith("- "), splitted_lines))
    if len(filter_quote) == len(splitted_lines):
        return BlockType.QUOTE
    if len(filter_unordered_list) == len(splitted_lines):
        return BlockType.UNORDERED_LIST
    ordered_list = False
    for i, l in enumerate(splitted_lines):
        num = i + 1
        digits = len(str(num))
        if len(l) < digits + 2:
            ordered_list = False
            break
        if l[:digits] == str(num) and l[digits] == "." and l[digits + 1] == " ":
            ordered_list = True
            continue
        ordered_list = False
        break
    if ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    parents = []
    for block in markdown_blocks:
        parents.append(block_to_html_node(block))
    return ParentNode("div", parents)

    
def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    lines = block.split("\n")
    match block_type:
        case BlockType.PARAGRAPH:
            new_block = " ".join(lines)
            text_nodes = text_to_textnodes(new_block)
            return ParentNode("p", text_to_children(text_nodes))
        case BlockType.HEADING:
            lvl = 0
            searching = True
            while searching:
                if block[lvl] == "#":
                    lvl += 1
                else:
                    searching = False

            text_nodes = text_to_textnodes(block[lvl + 1:])
            return ParentNode(f"h{lvl}", text_to_children(text_nodes))
        case BlockType.CODE:
            block = block[4:-3]
            text_node = TextNode(block, TextType.CODE)
            child = text_node_to_html_node(text_node)
            return ParentNode("pre", [child])
        case BlockType.QUOTE:
            quote = []
            new_lines = []
            for line in lines:
                if line.startswith("> "):
                    line = line[2:]
                else:
                    line = line[1:]

                new_lines.append(line)
                
            new_block = " ".join(new_lines)
            text_nodes = text_to_textnodes(new_block)
            return ParentNode("blockquote", text_to_children(text_nodes))
        case BlockType.UNORDERED_LIST:
            parents = []
            for l in lines:
                text_nodes = text_to_textnodes(l[2:])
                parents.append(ParentNode("li", text_to_children(text_nodes)))
            return ParentNode("ul", parents)
        case BlockType.ORDERED_LIST:
            parents = []
            for i, l in enumerate(lines):
                start = len(str(i + 1)) + 2
                text_nodes = text_to_textnodes(l[start:])
                parents.append(ParentNode("li", text_to_children(text_nodes)))
            return ParentNode("ol", parents)
        case _:
            raise ValueError(f"invalid block type {block_node.text_type}")


def text_to_children(text_nodes: list[TextNode]) -> list[HTMLNode] :
    children = []
    for block_node in text_nodes:
        child_node = text_node_to_html_node(block_node)
        children.append(child_node)
    return children


