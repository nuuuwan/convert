import os

from test_abstract_doc import TEST_DOC


def helper_test_rotation(helped_self, cls, file_name: str):
    doc1 = TEST_DOC
    doc2 = cls(doc1.paragraphs)
    helped_self.assertEqual(doc1.md5, doc2.md5)
    file_path = os.path.join("tests", "examples-output", file_name)
    doc2.to_file(file_path)
    doc3 = cls.from_file(file_path)
    helped_self.assertEqual(doc1.md5, doc3.md5)
