import re
from textnode import TextNode, TextType

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

            
def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        matches = extract_markdown_images(n.text)
        if len(matches) == 0:
            new_nodes.append(n)
            continue
        splitted_nodes = []
        text = n.text
        while matches:
            tup = matches.pop(0)
            delimiter = f"![{tup[0]}]({tup[1]})"
            splitted_text = text.split(delimiter, 1)
            if splitted_text[0] != "":
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(TextNode(tup[0], TextType.IMAGE, tup[1]))
            text = splitted_text[1]
        new_nodes.extend(splitted_nodes)
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        matches = extract_markdown_links(n.text)
        if len(matches) == 0:
            new_nodes.append(n)
            continue
        splitted_nodes = []
        text = n.text
        while matches:
            tup = matches.pop(0)
            delimiter = f"[{tup[0]}]({tup[1]})"
            splitted_text = text.split(delimiter, 1)
            if splitted_text[0] != "":
                splitted_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            splitted_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))
            text = splitted_text[1]
        new_nodes.extend(splitted_nodes)
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)] 
    for delimiter in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter[0], delimiter[1])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes



