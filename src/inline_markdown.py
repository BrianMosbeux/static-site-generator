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

            
