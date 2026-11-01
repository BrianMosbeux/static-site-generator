from textnode import TextNode, TextType
import os
from copy_content import copy_content
from generate_page import generate_pages_recursive


def main():
    cwd = os.getcwd()
    static_path = os.path.join(cwd, "static")
    public_path = os.path.join(cwd, "public")
    content_path = os.path.join(cwd, "content")
    template_path = os.path.join(cwd, "template.html")
    copy_content(static_path, public_path)
    generate_pages_recursive(content_path, template_path, public_path)

main()
