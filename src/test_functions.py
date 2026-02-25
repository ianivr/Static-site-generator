import unittest
from functions import split_nodes_delimiter
from textnode import TextNode, TextType


class TestFunctions(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    # --- Delimitador al inicio o al final ---

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text at the end **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("text at the end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    # --- Múltiples ocurrencias ---

    def test_multiple_delimiters(self):
        node = TextNode("a `one` and `two` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    # --- Nodo sin delimitador (no debe cambiar) ---

    def test_no_delimiter_in_text(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("Just plain text", TextType.TEXT),
        ])

    # --- Nodos que no son TEXT se pasan tal cual ---

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("already bold", TextType.BOLD),
        ])

    def test_mixed_node_types(self):
        nodes = [
            TextNode("plain text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("text with `code` here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("plain text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    # --- Delimitador no balanceado debe lanzar excepción ---

    def test_unbalanced_delimiter_raises(self):
        node = TextNode("This has `unbalanced delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_unbalanced_bold_raises(self):
        node = TextNode("This has **unbalanced bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    # --- Lista vacía ---

    def test_empty_list(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()