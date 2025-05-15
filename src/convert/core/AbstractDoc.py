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

    def split(self, max_words_per_part: int = 10_000) -> list["AbstractDoc"]:
        current_n_words = 0
        current_paragraphs = []
        docs = []

        for paragraph in self.paragraphs:
            n_words = paragraph.n_words
            if current_n_words + n_words <= max_words_per_part:
                current_paragraphs.append(paragraph)
                current_n_words += n_words
            else:
                docs.append(AbstractDoc(current_paragraphs))
                current_paragraphs = [paragraph]
                current_n_words = n_words

        if current_paragraphs:
            docs.append(AbstractDoc(current_paragraphs))
        log.info(f"Split into {len(docs)} parts")
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
        combined.export(doc_audio_file_path, format="mp3", bitrate="24k")
        file_size = os.path.getsize(doc_audio_file_path)
        log.info(f"Wrote {doc_audio_file_path} ({file_size/1_000_000:.3f}MB)")

    def to_audio_files(
        self, file_path_prefix: str, max_words_per_part: int = 10_000
    ) -> None:
        docs = self.split(max_words_per_part)
        for i, doc in enumerate(docs, start=1):
            file_path = f"{file_path_prefix}.part-{i:02d}.mp3"
            log.info(f"Building {file_path}...")
            doc.to_audio_file(file_path)

        log.info(f"Exported {len(docs)} to {file_path_prefix}")
