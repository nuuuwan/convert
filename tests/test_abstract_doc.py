import os
import unittest

from convert import AbstractDoc
from convert.core.Paragraph import Paragraph

TEST_DOC = AbstractDoc(
    paragraphs=[
        Paragraph(tag="h1", text="Sri Lanka"),
        Paragraph(tag="h2", text="Colombo"),
        Paragraph(tag="p", text="Colombo is the largest city in Sri Lanka."),
    ]
)
TEST_WORD_SET = {
    "colombo",
    "sri",
    "the",
    "lanka",
    "is",
    "largest",
    "in",
    "city",
}


class TestCaseAbstractDoc(unittest.TestCase):
    def test_words_set(self):

        self.assertEqual(TEST_DOC.n_words, 11)

        self.assertEqual(
            TEST_DOC.word_set,
            TEST_WORD_SET,
        )

        self.assertEqual(TEST_DOC.n_unique_words, 8)
        self.assertEqual(TEST_DOC.n_paragraphs, 3)
        self.assertAlmostEqual(TEST_DOC.n_words_per_paragraph, 11 / 3)
        self.assertAlmostEqual(TEST_DOC.n_unique_words_per_paragraph, 8 / 3)

        self.assertEqual(
            TEST_DOC.word_to_n,
            {"colombo": 2, "lanka": 2, "sri": 2, "city": 1, "largest": 1},
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
