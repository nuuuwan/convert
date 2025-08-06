import os
import unittest

from convert import AbstractDoc
from convert.core.Paragraph import Paragraph

TEST_DOC = AbstractDoc(
    paragraphs=[
        Paragraph(tag="h1", text="Sri Lanka"),
        Paragraph(tag="h2", text="1. Colombo"),
        Paragraph(tag="p", text="Colombo is the largest city in Sri Lanka."),
        Paragraph(tag="h2", text="2. Anuradhapura"),
        Paragraph(
            tag="p",
            text="Anuradhapura is the first capital city of Sri Lanka.",
        ),
    ]
)
E_WORD_SET = {
    "anuradhapura",
    "capital",
    "city",
    "colombo",
    "first",
    "in",
    "is",
    "lanka",
    "largest",
    "of",
    "sri",
    "the",
}

E_N_WORDS = 21
E_N_UNIQUE_WORDS = 12
E_N_PARAGRAPHS = 5

E_WORD_TO_N = {
    "lanka": 3,
    "sri": 3,
    "anuradhapura": 2,
    "city": 2,
    "colombo": 2,
    "capital": 1,
    "first": 1,
    "largest": 1,
}


class TestCaseAbstractDoc(unittest.TestCase):
    def test_words_set(self):

        self.assertEqual(TEST_DOC.n_words, E_N_WORDS)
        print(TEST_DOC.word_set)
        self.assertEqual(TEST_DOC.word_set, E_WORD_SET)

        self.assertEqual(TEST_DOC.n_unique_words, E_N_UNIQUE_WORDS)
        self.assertEqual(TEST_DOC.n_paragraphs, E_N_PARAGRAPHS)
        self.assertAlmostEqual(
            TEST_DOC.n_words_per_paragraph, E_N_WORDS / E_N_PARAGRAPHS
        )
        self.assertAlmostEqual(
            TEST_DOC.n_unique_words_per_paragraph,
            E_N_UNIQUE_WORDS / E_N_PARAGRAPHS,
        )
        print(TEST_DOC.word_to_n)
        self.assertEqual(TEST_DOC.word_to_n, E_WORD_TO_N)

    def test_to_audio_file(self):

        TEST_DOC.to_audio_file(
            os.path.join("tests", "examples-output", "test-sri-lanka.mp3")
        )

    def test_to_audio_files(self):
        TEST_DOC.to_audio_files(
            os.path.join("tests", "examples-output", "test-sri-lanka-parts"),
            20,
        )

    def test_level_up(self):
        doc = TEST_DOC.level_up()
        doc.paragraphs = [
            Paragraph(tag="h1", text="Sri Lanka"),
            Paragraph(tag="h1", text="1. Colombo"),
            Paragraph(
                tag="p", text="Colombo is the largest city in Sri Lanka."
            ),
            Paragraph(tag="h1", text="2. Anuradhapura"),
            Paragraph(
                tag="p",
                text="Anuradhapura is the first capital city of Sri Lanka.",
            ),
        ]

    def test_level_down(self):
        doc = TEST_DOC.level_down()
        doc.paragraphs = [
            Paragraph(tag="h2", text="Sri Lanka"),
            Paragraph(tag="h3", text="1. Colombo"),
            Paragraph(
                tag="p", text="Colombo is the largest city in Sri Lanka."
            ),
            Paragraph(tag="h3", text="2. Anuradhapura"),
            Paragraph(
                tag="p",
                text="Anuradhapura is the first capital city of Sri Lanka.",
            ),
        ]
