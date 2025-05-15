import os
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, Log
import tempfile
from gtts import gTTS

log = Log("AbstractDoc")


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
        file_path = os.path.join(
            tempfile.gettempdir(), f"paragraph.{self.md5}.mp3"
        )

        if force or not os.path.exists(file_path):
            tts = gTTS(self.text)
            tts.save(file_path)
            log.debug(f'"{self.text}" -> {file_path}')

        return file_path


@dataclass
class AbstractDoc(ABC):
    paragraphs: list[Paragraph]

    @cached_property
    def md5(self) -> str:
        return Hash.md5(
            "".join([paragraph.md5 for paragraph in self.paragraphs])
        )

    @cached_property
    def n_words(self) -> str:
        return sum([paragraph.n_words for paragraph in self.paragraphs])

    @classmethod
    def from_instance(cls, instance) -> None:
        return cls(instance.paragraphs)

    def clean(self):
        new_paragraphs = []
        has_started = False
        for paragraph in self.paragraphs:
            new_paragraph = paragraph.clean()
            if new_paragraph:
                if (
                    not has_started
                    and new_paragraph.text != "..."
                    and new_paragraph.text != "---"
                ):
                    has_started = True
                if has_started:
                    new_paragraphs.append(new_paragraph)
        self.paragraphs = new_paragraphs
        return self

    @classmethod
    def from_dir(cls, dir_path: str) -> None:
        paragraphs = []
        n_docs = 0
        for filename in os.listdir(dir_path):
            if filename.endswith(cls.get_ext()):
                file_path = os.path.join(dir_path, filename)
                doc = cls.from_file(file_path)
                doc.clean()
                doc.to_file(file_path)

                for paragraph in doc.paragraphs:
                    paragraphs.append(paragraph)
                n_docs += 1

        new_doc = cls(paragraphs)
        log.info(f"n_docs={n_docs:,}, n_words={new_doc.n_words:,}")
        return new_doc

    def to_audio_files(self, max_words_per_part: int = 10_000) -> None:
        pass
