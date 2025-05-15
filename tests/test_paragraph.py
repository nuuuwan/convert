import unittest
from convert.core.AbstractDoc import Paragraph
import os


class TestCase(unittest.TestCase):
    def test_get_temp_audio_file_path(self):
        paragraph = Paragraph(tag="p", text="Hello world")
        temp_audio_file_path = paragraph.get_temp_audio_file_path(force=True)
        self.assertTrue(os.path.exists(temp_audio_file_path))
