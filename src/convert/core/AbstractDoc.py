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
                paragraphs.extend(doc.paragraphs)
                n_docs += 1

                log.debug(f"{n_docs}) {doc.n_words:,}\t{filename}")

        new_doc = cls(paragraphs)
        log.info(f"n_docs={n_docs:,}, n_words={new_doc.n_words:,}")
        return new_doc
