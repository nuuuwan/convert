from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, Log

from convert.core.AbstractDocAudio import AbstractDocAudio
from convert.core.Paragraph import Paragraph

log = Log("AbstractDoc")


@dataclass
class AbstractDoc(ABC, AbstractDocAudio):
    paragraphs: list[Paragraph]

    @cached_property
    def md5(self) -> str:
        return Hash.md5(
            "".join([paragraph.md5 for paragraph in self.paragraphs])
        )

    @cached_property
    def n_words(self) -> str:
        return sum([paragraph.n_words for paragraph in self.paragraphs])

    @cached_property
    def word_set(self) -> set:
        word_set = set()
        for paragraph in self.paragraphs:
            word_set.update(paragraph.word_set)
        return word_set

    @cached_property
    def n_unique_words(self) -> int:
        return len(self.word_set)

    @cached_property
    def n_paragraphs(self) -> int:
        return len(self.paragraphs)

    @cached_property
    def n_words_per_paragraph(self) -> int:
        return (
            self.n_words / self.n_paragraphs if self.n_paragraphs > 0 else 0
        )

    @cached_property
    def n_unique_words_per_paragraph(self) -> int:
        return (
            self.n_unique_words / self.n_paragraphs
            if self.n_paragraphs > 0
            else 0
        )

    @cached_property
    def word_to_n(self) -> dict:
        word_to_n = {}
        for paragraph in self.paragraphs:
            for word, n in paragraph.word_to_n.items():
                if word not in word_to_n:
                    word_to_n[word] = 0
                word_to_n[word] += n

        word_to_n = {
            k: v
            for k, v in sorted(
                word_to_n.items(),
                key=lambda item: (-item[1], item[0]),
            )
        }
        return word_to_n

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

    def level_up(self):
        return self.__class__(
            [paragraph.level_up() for paragraph in self.paragraphs]
        )

    def level_down(self):
        return self.__class__(
            [paragraph.level_down() for paragraph in self.paragraphs]
        )
