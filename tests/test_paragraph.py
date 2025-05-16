import os
import unittest

from convert.core.Paragraph import Paragraph


class TestCase(unittest.TestCase):
    def test_get_temp_audio_file_path(self):
        paragraph = Paragraph(tag="p", text="Hello, Hello, world.")
        temp_audio_file_path = paragraph.get_temp_audio_file_path(force=True)
        self.assertTrue(os.path.exists(temp_audio_file_path))

        self.assertEqual(paragraph.words, ["hello", "hello", "world"])
        self.assertEqual(paragraph.n_words, 3)
        self.assertEqual(paragraph.word_set, {"hello", "world"})
        self.assertEqual(paragraph.n_unique_words, 2)
