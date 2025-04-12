import os
import unittest

from convert import DocXDoc, MarkdownDoc


class TestCase(unittest.TestCase):
    TEST_DOCX_DOC = DocXDoc.from_file(
        os.path.join("tests", "examples", "test.docx")
    )
    TEST_MARKDOWN_DOC = MarkdownDoc.from_file(
        os.path.join("tests", "examples", "test.md")
    )

    def test_md_to_docx(self):
        doc = MarkdownDoc.from_instance(self.TEST_MARKDOWN_DOC)
        doc2 = DocXDoc.from_instance(doc)

        doc2_path = os.path.join("tests", "examples", "test2.docx")
        doc2.to_file(doc2_path)
        doc3 = DocXDoc.from_file(doc2_path)

        self.assertEqual(doc3.md5, doc.md5)

    def test_docx_to_md(self):
        doc = DocXDoc.from_instance(self.TEST_DOCX_DOC)
        doc2 = MarkdownDoc.from_instance(doc)

        doc2_path = os.path.join("tests", "examples", "test2.md")
        doc2.to_file(doc2_path)
        doc3 = MarkdownDoc.from_file(doc2_path)

        self.assertEqual(doc3.md5, doc.md5)
