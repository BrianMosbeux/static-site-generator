def markdown_to_blocks(markdown: str) -> list[str]:
    splitted_markdown = markdown.split("\n\n")
    stripped_markdown = [s.strip() for s in splitted_markdown if s != ""]
    return stripped_markdown


