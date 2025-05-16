import os
import unittest

from convert import AbstractDoc
from convert.core.Paragraph import Paragraph

TEST_DOC = AbstractDoc(
    paragraphs=[
        Paragraph(tag="h1", text="Sri Lanka"),
        Paragraph(tag="p", text="Sri Lanka is a country in South Asia."),
        Paragraph(tag="p", text=""),
        Paragraph(tag="p", text="It is located in the Indian Ocean."),
        Paragraph(tag="h1", text="Colombo"),
        Paragraph(tag="p", text="Colombo is the largest city in Sri Lanka."),
    ]
)


class TestCase(unittest.TestCase):
    def test_to_audio_file(self):

        TEST_DOC.to_audio_file(
            os.path.join("tests", "examples", "test-sri-lanka.mp3")
        )

    def test_to_audio_files(self):
        TEST_DOC.to_audio_files(
            os.path.join("tests", "examples", "test-sri-lanka-parts"),
            20,
        )
