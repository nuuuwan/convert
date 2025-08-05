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
TEST_WORD_SET = {
    "a",
    "asia",
    "city",
    "colombo",
    "country",
    "in",
    "indian",
    "is",
    "it",
    "lanka",
    "largest",
    "located",
    "ocean",
    "south",
    "sri",
    "the",
}


class TestCase(unittest.TestCase):
    def test_words_set(self):

        self.assertEqual(TEST_DOC.n_words, 26)

        self.assertEqual(
            TEST_DOC.word_set,
            TEST_WORD_SET,
        )

        self.assertEqual(TEST_DOC.n_unique_words, 16)
        self.assertEqual(TEST_DOC.n_paragraphs, 6)
        self.assertAlmostEqual(TEST_DOC.n_words_per_paragraph, 26 / 6)
        self.assertAlmostEqual(TEST_DOC.n_unique_words_per_paragraph, 16 / 6)

        self.assertEqual(
            TEST_DOC.word_to_n,
            {
                "lanka": 3,
                "sri": 3,
                "colombo": 2,
                "asia": 1,
                "city": 1,
                "country": 1,
                "indian": 1,
                "largest": 1,
                "located": 1,
                "ocean": 1,
                "south": 1,
            },
        )

    def test_to_audio_file(self):

        TEST_DOC.to_audio_file(
            os.path.join("tests", "examples", "test-sri-lanka.mp3")
        )

    def test_to_audio_files(self):
        TEST_DOC.to_audio_files(
            os.path.join("tests", "examples", "test-sri-lanka-parts"),
            20,
        )
