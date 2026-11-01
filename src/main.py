from textnode import TextNode, TextType
import os
from copy_content import copy_content
from generate_page import generate_pages_recursive
import sys


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1] 
    else:
        basepath = "/"
    static_path = "static"
    public_path = "docs"
    content_path = "content"
    template_path = "template.html"
    copy_content(static_path, public_path)
    generate_pages_recursive(basepath, content_path, template_path, public_path)

main()
