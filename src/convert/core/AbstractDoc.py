import os
from abc import ABC
from dataclasses import dataclass
from functools import cached_property

from pydub import AudioSegment
from utils import Hash, Log

from convert.core.Paragraph import Paragraph

log = Log("AbstractDoc")


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

    def split_by_header_group(self) -> list["AbstractDoc"]:
        current_paragraphs = []
        docs = []
        for paragraph in self.paragraphs:
            if paragraph.tag.startswith("h"):
                if current_paragraphs:
                    docs.append(AbstractDoc(current_paragraphs))
                current_paragraphs = [paragraph]
            else:
                current_paragraphs.append(paragraph)

        if current_paragraphs:
            docs.append(AbstractDoc(current_paragraphs))
        log.info(f"Split into {len(docs)} header groups")
        return docs

    def split(self, max_words: int) -> list["AbstractDoc"]:
        docs_by_header_group = self.split_by_header_group()
        docs = []
        current_n_words = 0
        current_doc = None

        for doc in docs_by_header_group:
            if doc.n_words + current_n_words <= max_words:
                current_n_words += doc.n_words
                if current_doc:
                    current_doc.paragraphs.extend(doc.paragraphs)
                else:
                    current_doc = doc
            else:
                if current_doc:
                    docs.append(current_doc)
                current_doc = doc
                current_n_words = doc.n_words

        if current_doc:
            docs.append(current_doc)

        log.info(f"Split into {len(docs)} of max_words={max_words:,}")
        return docs

    def to_audio_file(self, doc_audio_file_path: str) -> None:
        assert doc_audio_file_path.endswith(
            ".mp3"
        ), "File path must end with .mp3"

        combined = AudioSegment.empty()
        DIR_MEDIA = os.path.join(
            os.environ["DIR_PY"],
            "convert",
            "media",
        )
        LONG_BELL_AUDIO_SEGMENT = AudioSegment.from_file(
            os.path.join(
                DIR_MEDIA,
                "tabla-long.mp3",
            )
        )
        SHORT_BELL_AUDIO_SEGMENT = AudioSegment.from_file(
            os.path.join(
                DIR_MEDIA,
                "tabla-short.mp3",
            )
        )
        SILENT_AUDIO_SEGMENT = AudioSegment.silent(duration=1000)

        for paragraph in self.paragraphs:

            if paragraph.text == "...":
                combined += SILENT_AUDIO_SEGMENT
                combined += SHORT_BELL_AUDIO_SEGMENT
                combined += SILENT_AUDIO_SEGMENT
                continue

            if paragraph.tag != "p":
                combined += SILENT_AUDIO_SEGMENT
                combined += LONG_BELL_AUDIO_SEGMENT
                combined += SILENT_AUDIO_SEGMENT

            paragraph_audio_file_path = paragraph.get_temp_audio_file_path()
            if not paragraph_audio_file_path:
                continue
            assert paragraph_audio_file_path.endswith(
                ".mp3"
            ), "File path must end with .mp3"
            if not os.path.exists(paragraph_audio_file_path):
                log.warning(
                    f"File {paragraph_audio_file_path} does not exist. Skipping."
                )
                continue
            file_size = os.path.getsize(paragraph_audio_file_path)
            if file_size == 0:
                log.warning(f"File {paragraph_audio_file_path} is empty")
                continue
            audio = AudioSegment.from_file(paragraph_audio_file_path)
            combined += audio

            if paragraph.tag != "p":
                combined += SILENT_AUDIO_SEGMENT

        combined += SILENT_AUDIO_SEGMENT
        combined += LONG_BELL_AUDIO_SEGMENT
        combined.export(doc_audio_file_path, format="mp3", bitrate="16k")
        file_size = os.path.getsize(doc_audio_file_path)
        log.info(f"Wrote {doc_audio_file_path} ({file_size/1_000_000:.3f}MB)")

    def to_audio_files(
        self, file_path_prefix: str, max_words_per_part: int
    ) -> None:
        docs = self.split(max_words_per_part)
        for i, doc in enumerate(docs, start=1):
            file_path = f"{file_path_prefix}.part-{i:02d}.mp3"
            log.info(f"Building {file_path}...")
            doc.to_audio_file(file_path)

        log.info(f"Exported {len(docs)} to {file_path_prefix}")
