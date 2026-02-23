import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="This is a paragraph")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_not_eq(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"class": "text"})
        node2 = HTMLNode(tag="p", value="This is a different paragraph", props={"class": "text"})
        self.assertNotEqual(node, node2)

    def test_prop_to_html(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"class": "text", "id": "intro"})
        expected = ' class="text" id="intro"'
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
