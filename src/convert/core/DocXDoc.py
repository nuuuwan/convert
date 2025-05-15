import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from utils import Log, Time, TimeFormat

from convert.core.AbstractDoc import AbstractDoc
from convert.core.Paragraph import Paragraph

log = Log("DocXDoc")


class DocXDoc(AbstractDoc):
    TEMPLATE_PATH = os.path.join(
        "src", "convert", "core", "docx_template.docx"
    )

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
        doc = cls(paragraphs)
        doc.clean()
        return doc

    def add_title_etc(self, doc: Document) -> None:
        title = doc.add_paragraph("The Lies You Told Me")
        title.style = "Custom Title"

        author = doc.add_paragraph("Nuwan I. Senaratna")
        author.style = "Custom Title Author"

        date = doc.add_paragraph(TimeFormat("%b %d, %Y").format(Time.now()))
        date.style = "Custom Title Date"

        doc.add_page_break()

    def to_file(self, file_path: str, add_title=False) -> None:
        doc = Document(self.TEMPLATE_PATH)

        if add_title:
            self.add_title_etc(doc)

        for paragraph in self.paragraphs:
            if paragraph.tag.startswith("h"):
                level = int(paragraph.tag[1])
                doc.add_heading(paragraph.text, level=level)
            else:
                p = doc.add_paragraph(paragraph.text)
                if paragraph.text == "...":
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.save(file_path)
