import os
import unittest

from convert import DocXDoc


class TestCase(unittest.TestCase):
    TEST_DOCX_DOC = DocXDoc.from_file(
        os.path.join("tests", "examples", "test.docx")
    )

    def test_hash(self):
        doc = self.TEST_DOCX_DOC
        self.assertEqual(doc.md5, "ea8b7080a84d0fefd8e03fa334be63ca")

    def test_from_file(self):
        doc = self.TEST_DOCX_DOC
        self.assertEqual(len(doc.paragraphs), 4)

    def test_to_file(self):
        doc = self.TEST_DOCX_DOC
        doc2_path = os.path.join("tests", "examples-output", "test2.docx")
        doc.to_file(doc2_path)
        doc2 = DocXDoc.from_file(doc2_path)
        self.assertEqual(doc2.md5, doc.md5)
