from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"   


def markdown_to_blocks(markdown: str) -> list[str]:
    splitted_markdown = markdown.split("\n\n")
    stripped_markdown = [s.strip() for s in splitted_markdown if s != ""]
    return stripped_markdown

def block_to_block_type(block: str) -> BlockType:
    if block == "":
        return BlockType.PARAGRAPH
    if block[0] == "#":
        for char in block[:7]:
            if char == "#":
                continue
            if char == " ":
                return BlockType.HEADING
            break

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
        if len(l) < digits + 1:
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



    

