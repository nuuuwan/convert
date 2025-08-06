import os
import unittest

from convert import TexDoc
from tests.test_abstract_doc import TEST_DOC


class TestCase(unittest.TestCase):

    def test_to_file(self):

        doc2 = TexDoc.from_instance(TEST_DOC)
        doc2.to_file(os.path.join("tests", "examples-output", "test2.tex"))
        self.assertTrue(
            os.path.exists(
                os.path.join("tests", "examples-output", "test2.tex")
            )
        )
