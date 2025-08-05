import os
import unittest

from convert import MarkdownDirDoc


class TestCase(unittest.TestCase):
    TEST_MARKDOWN_DIR_DOC = MarkdownDirDoc.from_file(
        os.path.join("tests", "examples", "test_md_dir")
    )

    def test_hash(self):
        doc = self.TEST_MARKDOWN_DIR_DOC
        self.assertEqual(doc.md5, "48310a0a52581492e774c231d5107d8e")

    def test_from_file(self):
        doc = self.TEST_MARKDOWN_DIR_DOC
        self.assertEqual(len(doc.paragraphs), 8)

    def test_to_file(self):
        doc = self.TEST_MARKDOWN_DIR_DOC
        doc2_path = os.path.join("tests", "examples-output", "test2_md_dir")
        doc.to_file(doc2_path)
        doc2 = MarkdownDirDoc.from_file(doc2_path)
        self.assertEqual(doc2.md5, doc.md5)
