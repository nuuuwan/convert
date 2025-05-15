import os
import tempfile
from dataclasses import dataclass
from functools import cached_property

from gtts import gTTS
from utils import Hash, Log

log = Log("Paragraph")


@dataclass
class Paragraph:
    tag: str
    text: str

    @cached_property
    def md5(self) -> str:
        return Hash.md5(self.tag + ":" + self.text)

    @cached_property
    def n_words(self) -> int:
        return len(self.text.split())

    def clean(self):
        text = self.text.strip()

        for before, after in [
            ("\n---\n", "\n...\n"),
            ("“", '"'),
            ("”", '"'),
            ("‘", "'"),
            ("’", "'"),
            ("…", "..."),
            ("*", ""),
            ("> ", ""),
            ("_", ""),
            ("—", "-"),
        ]:
            text = text.replace(before, after)

        if text:
            return Paragraph(self.tag, text)
        return None

    @staticmethod
    def get_lower_tag(tag):
        if tag == "h1":
            return "h2"
        elif tag == "h2":
            return "h3"
        return "p"

    def lower(self):
        return Paragraph(Paragraph.get_lower_tag(self.tag), self.text)

    def get_temp_audio_file_path(self, force=False):
        if self.text == "":
            return None

        file_path = os.path.join(
            tempfile.gettempdir(), f"paragraph.{self.md5}.mp3"
        )

        if force or not os.path.exists(file_path):
            try:
                tts = gTTS(self.text)
                tts.save(file_path)
                print(f'"{self.text[:10]}..." -> {file_path}', end="\r")
            except Exception as e:
                log.error(f"Error: {e}")
                return None
        return file_path
