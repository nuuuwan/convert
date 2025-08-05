import os
import re
import tempfile
from dataclasses import dataclass
from functools import cached_property

from gtts import gTTS
from utils import Hash, Log

from convert.core.StopWords import StopWords

log = Log("Paragraph")


@dataclass
class Paragraph:
    tag: str
    text: str

    @cached_property
    def md5(self) -> str:
        return Hash.md5(self.tag + ":" + self.text)

    @cached_property
    def words(self) -> list:
        # replace non-alphabetical
        x = self.text.lower()
        x = re.sub(r"'", "", x)
        x = re.sub(r"[^a-z\s]", " ", x)
        return x.split()

    @cached_property
    def word_to_n(self) -> dict:
        word_to_n = {}
        for word in self.words:
            if word in StopWords.SET:
                continue
            if word not in word_to_n:
                word_to_n[word] = 0
            word_to_n[word] += 1
        return word_to_n

    @cached_property
    def word_set(self) -> set:
        return set(self.words)

    @cached_property
    def n_words(self) -> int:
        return len(self.words)

    @cached_property
    def n_unique_words(self) -> int:
        return len(self.word_set)

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

    def __get_temp_audio_file_path_hot__(self, file_path):

        try:
            slow = False if self.tag == "p" else True

            tts = gTTS(self.text, slow=slow)
            tts.save(file_path)

            file_size = os.path.getsize(file_path)
            if file_size < 10:
                raise Exception(f'("{self.text}") File size is too small')
            print(f'"{self.text[:10]}..." -> "{file_path}"', end="\r")
            return file_path
        except Exception as e:
            log.error(f'("{self.text}") {e}')
            return None

    def get_temp_audio_file_path(self, force: bool = False):
        if self.text.strip() in ["", "...", "---"]:
            return None

        file_path = os.path.join(
            tempfile.gettempdir(), f"paragraph.{self.md5}.mp3"
        )
        if not force and os.path.exists(file_path):
            return file_path

        return self.__get_temp_audio_file_path_hot__(file_path)
