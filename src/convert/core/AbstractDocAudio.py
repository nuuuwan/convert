import os

from pydub import AudioSegment
from utils import Log

log = Log("AbstractDocAudio")


class AbstractDocAudio:
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

    def split_by_header_group(self) -> list["AbstractDocAudio"]:
        cls = self.__class__
        current_paragraphs = []
        docs = []
        for paragraph in self.paragraphs:
            if paragraph.tag.startswith("h"):
                if current_paragraphs:
                    docs.append(cls(current_paragraphs))
                current_paragraphs = [paragraph]
            else:
                current_paragraphs.append(paragraph)

        if current_paragraphs:
            docs.append(cls(current_paragraphs))
        log.info(f"Split into {len(docs)} header groups")
        return docs

    def split(self, max_words: int) -> list["AbstractDocAudio"]:
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

        for paragraph in self.paragraphs:

            if paragraph.text == "...":
                combined += self.SILENT_AUDIO_SEGMENT
                combined += self.SHORT_BELL_AUDIO_SEGMENT
                combined += self.SILENT_AUDIO_SEGMENT
                continue

            if paragraph.tag != "p":
                combined += self.SILENT_AUDIO_SEGMENT
                combined += self.LONG_BELL_AUDIO_SEGMENT
                combined += self.SILENT_AUDIO_SEGMENT

            paragraph_audio_file_path = paragraph.get_temp_audio_file_path()
            if not paragraph_audio_file_path:
                continue
            assert paragraph_audio_file_path.endswith(
                ".mp3"
            ), "File path must end with .mp3"
            if not os.path.exists(paragraph_audio_file_path):
                log.warning(
                    f"File {paragraph_audio_file_path} does not exist. Skip."
                )
                continue
            file_size = os.path.getsize(paragraph_audio_file_path)
            if file_size == 0:
                log.warning(f"File {paragraph_audio_file_path} is empty")
                continue
            audio = AudioSegment.from_file(paragraph_audio_file_path)
            combined += audio

            if paragraph.tag != "p":
                combined += self.SILENT_AUDIO_SEGMENT

        combined += self.SILENT_AUDIO_SEGMENT
        combined += self.LONG_BELL_AUDIO_SEGMENT
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
