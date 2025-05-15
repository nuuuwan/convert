import unittest
import os
from convert import AbstractDoc
from convert.core.AbstractDoc import Paragraph

TEST_DOC = AbstractDoc(
    paragraphs=[
        Paragraph(tag="p", text="Hello Sri Lanka!"),
        Paragraph(tag="p", text=""),
        Paragraph(tag="p", text="This is a test"),
    ]
)


class TestCase(unittest.TestCase):
    def test_to_audio_file(self):

        TEST_DOC.to_audio_file(os.path.join("tests", "examples", "test.mp3"))

    def test_to_audio_files(self):
        TEST_DOC.to_audio_files(
            os.path.join("tests", "examples", "test-parts"),
            3,
        )
