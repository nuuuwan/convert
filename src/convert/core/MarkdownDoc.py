from utils import File, Log

from convert.core.AbstractDoc import AbstractDoc, Paragraph

log = Log("MarkdownDoc")


class MarkdownDoc(AbstractDoc):
    @classmethod
    def get_ext(cls) -> str:
        return ".md"

    @staticmethod
    def parse_line(line: str) -> Paragraph:
        if line.startswith("# "):
            return Paragraph("h1", line[2:].strip())
        if line.startswith("## "):
            return Paragraph("h2", line[3:].strip())
        if line.startswith("### "):
            return Paragraph("h3", line[4:].strip())
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
        if paragraph.tag == "h1":
            return f"# {paragraph.text}\n"
        if paragraph.tag == "h2":
            return f"## {paragraph.text}\n"
        if paragraph.tag == "h3":
            return f"### {paragraph.text}\n"
        return f"{paragraph.text}\n"

    def to_file(self, file_path: str) -> None:
        lines = []
        for paragraph in self.paragraphs:
            line = MarkdownDoc.write_line(paragraph)
            lines.append(line)
        File(file_path).write_lines(lines)
