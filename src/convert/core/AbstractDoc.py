from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash


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

    @cached_property
    def md5(self) -> str:
        return Hash.md5(
            "".join([paragraph.md5 for paragraph in self.paragraphs])
        )

    @classmethod
    def from_instance(cls, instance) -> None:
        return cls(instance.paragraphs)
