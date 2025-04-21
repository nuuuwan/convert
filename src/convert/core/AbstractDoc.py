import os
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, Log

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
        for paragraph in self.paragraphs:
            new_paragraph = paragraph.clean()
            if new_paragraph:
                new_paragraphs.append(new_paragraph)
        self.paragraphs = new_paragraphs
        return self

    @classmethod
    def from_dir(cls, dir_path: str) -> None:
        paragraphs = []
        n_docs = 0
        for filename in os.listdir(dir_path):
            if (
                filename.endswith(cls.get_ext())
                and filename[:4] != "_all"
                and filename[:6] != "README"
            ):
                file_path = os.path.join(dir_path, filename)
                doc = cls.from_file(file_path)
                doc.clean()
                doc.to_file(file_path)

                for paragraph in doc.paragraphs:
                    paragraphs.append(paragraph)
                n_docs += 1

                emoji = None
                if doc.n_words > 1_250:
                    emoji = "🔴"
                elif doc.n_words > 1_000:
                    emoji = "🟡"

                if emoji:
                    log.debug(f"{emoji}{n_docs})\t{doc.n_words:,}\t{filename}")

                if n_docs >= 10:
                    break

        new_doc = cls(paragraphs)
        log.info(f"n_docs={n_docs:,}, n_words={new_doc.n_words:,}")
        return new_doc
