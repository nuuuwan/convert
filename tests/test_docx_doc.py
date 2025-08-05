import os
import unittest

from convert import DocXDoc


class TestCase(unittest.TestCase):
    TEST_DOCX_DOC = DocXDoc.from_file(
        os.path.join("tests", "examples", "test.docx")
    )

    def test_hash(self):
        doc = self.TEST_DOCX_DOC
        self.assertEqual(doc.md5, "6e9efc73a40224922d1b3435d2cd43ed")

    def test_from_file(self):
        doc = self.TEST_DOCX_DOC
        self.assertEqual(len(doc.paragraphs), 3)

    def test_to_file(self):
        doc = self.TEST_DOCX_DOC
        doc2_path = os.path.join("tests", "examples-output", "test2.docx")
        doc.to_file(doc2_path)
        doc2 = DocXDoc.from_file(doc2_path)
        self.assertEqual(doc2.md5, doc.md5)
