from textnode import TextNode, TextType
from functions import copy_directory

def main():
    node = TextNode("Hello, World!", TextType.LINK, url="https://example.com")
    print(node)

    copy_directory("static", "public")

if __name__ == "__main__":
    main()