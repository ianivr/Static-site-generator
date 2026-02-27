from textnode import TextNode, TextType
from functions import copy_directory, generate_page

def main():
    node = TextNode("Hello, World!", TextType.LINK, url="https://example.com")
    print(node)

    copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()