from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, Log

log = Log("GenericDocFormat")


@dataclass
class Paragraph:
    tag: str
    text: str

    @cached_property
    def md5(self) -> str:
        return Hash.md5(self.tag + ":" + self.text)


@dataclass
class AbstractDoc(ABC):
    paragraphs: list[Paragraph]

    def read(self, file_path: str) -> None:
        raise NotImplementedError

    def write(self, file_path: str) -> None:
        raise NotImplementedError

    @cached_property
    def md5(self) -> str:
        return Hash.md5(
            "".join([paragraph.md5 for paragraph in self.paragraphs])
        )
