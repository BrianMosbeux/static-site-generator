from textnode import TextNode, TextType
import os
import shutil


def main():
    cwd = os.getcwd()
    static_path = os.path.join(cwd, "static")
    public_path = os.path.join(cwd, "public")
    copy_content(static_path, public_path)


def copy_content(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    content = os.listdir(source)
    for item in content:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        print(f"SOURCE: {source_path}")
        print(f"DESTINATION: {dest_path}")
        if os.path.isdir(source_path):
            copy_content(source_path, dest_path)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination)
main()
