import os
from blocks_markdown import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No H1 title was found on this file")



def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown:
        markdown_content = markdown.read()
    with open(template_path) as template:
        template_content = template.read()
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    new_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    new_path = os.path.dirname(dest_path)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    with open(dest_path, "w") as html_file:
        html_file.write(new_html)
        




    





