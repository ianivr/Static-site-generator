import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_not_eq(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"class": "text"})
        node2 = HTMLNode(
            tag="p", value="This is a different paragraph", props={"class": "text"}
        )
        self.assertNotEqual(node, node2)

    def test_prop_to_html(self):
        node = HTMLNode(
            tag="p", value="This is a paragraph", props={"class": "text", "id": "intro"}
        )
        expected = ' class="text" id="intro"'
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
