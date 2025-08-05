import os
import unittest

from convert import MarkdownDoc, TexDoc


class TestCase(unittest.TestCase):

    def test_to_file(self):

        doc2 = TexDoc.from_instance(
            MarkdownDoc.from_file(
                os.path.join("tests", "examples", "test.md")
            )
        )
        doc2.to_file(os.path.join("tests", "examples-output", "test2.tex"))
        self.assertTrue(
            os.path.exists(
                os.path.join("tests", "examples-output", "test2.tex")
            )
        )
