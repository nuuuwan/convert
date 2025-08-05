from utils import File, Log

from convert.core.AbstractDoc import AbstractDoc
from convert.core.Paragraph import Paragraph

log = Log("MarkdownDoc")


class MarkdownDoc(AbstractDoc):
    H_LEVELS = 4

    @classmethod
    def get_ext(cls) -> str:
        return ".md"

    @staticmethod
    def parse_line(line: str) -> Paragraph:
        for ih in range(0, MarkdownDoc.H_LEVELS):
            if line.startswith(f"{'#' * (ih + 1)} "):
                return Paragraph(f"h{ih + 1}", line[ih + 2:].strip())

        return Paragraph("p", line.strip())

    @classmethod
    def from_file(cls, file_path: str) -> None:
        assert file_path.endswith(cls.get_ext())
        paragraphs = []
        # HACK to fix unicode bug in File
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                if line.strip():
                    paragraph = MarkdownDoc.parse_line(line)
                    paragraphs.append(paragraph)
        doc = cls(paragraphs)
        doc.clean()
        return doc

    @staticmethod
    def write_line(paragraph: Paragraph) -> str:
        for ih in range(0, MarkdownDoc.H_LEVELS):
            if paragraph.tag == f"h{ih + 1}":
                return f"{'#' * (ih + 1)} {paragraph.text}\n"

        return f"{paragraph.text}\n"

    def to_file(self, file_path: str) -> None:
        lines = []
        for paragraph in self.paragraphs:
            line = MarkdownDoc.write_line(paragraph)
            lines.append(line)
        File(file_path).write_lines(lines)
