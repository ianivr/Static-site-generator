import unittest
from block import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):

    # Headings
    def test_h1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_h3(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)

    def test_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # Code
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_no_closing_is_paragraph(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    # Quote
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type(">some quote"), BlockType.QUOTE)

    def test_multiline_quote(self):
        self.assertEqual(block_to_block_type(">line one\n>line two\n>line three"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> quote with space"), BlockType.QUOTE)

    def test_quote_missing_gt_is_paragraph(self):
        self.assertEqual(block_to_block_type(">line one\nline two"), BlockType.PARAGRAPH)

    # Unordered list
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two\n- item three"), BlockType.UNORDERED_LIST)

    def test_unordered_missing_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-item\n- item"), BlockType.PARAGRAPH)

    # Ordered list
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_is_paragraph(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number_is_paragraph(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    # Paragraph
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text here."), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()