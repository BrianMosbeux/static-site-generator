from textnode import TextNode, TextType
import os
from copy_content import copy_content


def main():
    cwd = os.getcwd()
    static_path = os.path.join(cwd, "static")
    public_path = os.path.join(cwd, "public")
    copy_content(static_path, public_path)

main()
