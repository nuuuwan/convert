from docx import Document
from utils import Log

from convert.core.AbstractDoc import AbstractDoc, Paragraph

log = Log("DocXDoc")


class DocXDoc(AbstractDoc):
    @classmethod
    def get_ext(cls) -> str:
        return ".docx"

    @staticmethod
    def parse_docx_paragraph(docx_paragraph) -> Paragraph:
        if docx_paragraph.style.name.startswith("Heading"):
            level = int(docx_paragraph.style.name[-1])
            return Paragraph(f"h{level}", docx_paragraph.text)
        return Paragraph("p", docx_paragraph.text)

    @classmethod
    def from_file(cls, file_path: str) -> None:
        assert file_path.endswith(cls.get_ext())
        doc = Document(file_path)
        paragraphs = []
        for docx_paragraph in doc.paragraphs:
            if docx_paragraph.text.strip():
                paragraph = DocXDoc.parse_docx_paragraph(docx_paragraph)
                paragraphs.append(paragraph)
        return cls(paragraphs)

    def to_file(self, file_path: str) -> None:
        doc = Document()
        for paragraph in self.paragraphs:
            if paragraph.tag.startswith("h"):
                level = int(paragraph.tag[1])
                doc.add_heading(paragraph.text, level=level)
            else:
                doc.add_paragraph(paragraph.text)
        doc.save(file_path)
