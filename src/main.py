from textnode import TextNode, TextType
from functions import copy_directory, generate_pages_recursive

def main():
    node = TextNode("Hello, World!", TextType.LINK, url="https://example.com")
    print(node)

    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()