from block import BlockType, block_to_block_type
from textnode import TextNode, TextType, text_node_to_html_node
import re
from htmlnode import ParentNode
import os
import shutil


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)

            if len(parts) % 2 == 0:
                raise Exception(
                    f"Delimiter '{delimiter}' is not balanced in text: {node.text}"
                )

            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining = node.text
        for alt, url in images:
            parts = remaining.split(f"![{alt}]({url})", 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = parts[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining = node.text
        for anchor, url in links:
            parts = remaining.split(f"[{anchor}]({url})", 1)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = parts[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()
        if block != "":
            result.append(block)
    return result


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            text = block[level + 1 :]  # skip "# "
            node = ParentNode(f"h{level}", text_to_children(text))

        elif block_type == BlockType.CODE:
            code_text = block[3:-3].strip(
                "\n"
            )  # quita los ``` de ambos lados y el primer/último \n
            code_node = text_node_to_html_node(
                TextNode(code_text + "\n", TextType.CODE)
            )
            node = ParentNode("pre", [code_node])

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped = "\n".join(line.lstrip(">").strip() for line in lines)
            node = ParentNode("blockquote", text_to_children(stripped))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            items = [ParentNode("li", text_to_children(line[2:])) for line in lines]
            node = ParentNode("ul", items)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            items = [
                ParentNode("li", text_to_children(re.sub(r"^\d+\. ", "", line)))
                for line in lines
            ]
            node = ParentNode("ol", items)

        else:  # PARAGRAPH
            text = " ".join(block.split("\n"))
            node = ParentNode("p", text_to_children(text))

        block_nodes.append(node)

    return ParentNode("div", block_nodes)


def copy_directory(src, dst):
    # Delete destination directory if it exists and recreate it
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)
