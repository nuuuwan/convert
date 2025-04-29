from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
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

    @staticmethod
    def set_style(doc):

        FONT_NAME = "Book Antiqua"
        FONT_SIZE_NORMAL = 12

        normal_style = doc.styles["Normal"]
        normal_font = normal_style.font
        normal_font.name = FONT_NAME
        normal_font.size = Pt(FONT_SIZE_NORMAL)
        normal_font.color.rgb = RGBColor(0, 0, 0)

        heading1_style = doc.styles["Heading 1"]
        heading1_font = heading1_style.font
        heading1_font.name = FONT_NAME
        heading1_font.size = Pt(FONT_SIZE_NORMAL * 2)
        heading1_font.color.rgb = RGBColor(0, 0, 0)

        heading1_paragraph_format = heading1_style.paragraph_format
        heading1_paragraph_format.page_break_before = True

        heading1_font.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)
        # Remove theme font settings by deleting the attributes
        rFonts = heading1_font.element.rPr.rFonts
        for attr in ("w:asciiTheme", "w:hAnsiTheme"):
            if rFonts.get(qn(attr)):
                del rFonts.attrib[qn(attr)]

    def to_file(self, file_path: str) -> None:
        doc = Document()
        self.set_style(doc)

        for paragraph in self.paragraphs:
            if paragraph.tag.startswith("h"):
                level = int(paragraph.tag[1])
                doc.add_heading(paragraph.text, level=level)
            else:
                p = doc.add_paragraph(paragraph.text)
                if paragraph.text == "...":
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.save(file_path)
