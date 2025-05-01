from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from utils import Log, Time, TimeFormat
import os
from convert.core.AbstractDoc import AbstractDoc, Paragraph

log = Log("DocXDoc")


class DocXDoc(AbstractDoc):
    TEMPLATE_PATH = os.path.join("src", "convert", "core", "docx_template.docx")

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

        if "Custom Title" not in doc.styles:
            custom_title_style = doc.styles.add_style("Custom Title", 1)
            custom_title_font = custom_title_style.font
            custom_title_font.name = FONT_NAME
            custom_title_font.size = Pt(36)
            custom_title_font.color.rgb = RGBColor(0, 0, 0)
            custom_title_paragraph_format = custom_title_style.paragraph_format
            custom_title_paragraph_format.page_break_before = True
            custom_title_paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            custom_title_paragraph_format.space_before = Pt(240)

        # Create a custom style for the author
        if "Custom Title Author" not in doc.styles:
            custom_author_style = doc.styles.add_style("Custom Title Author", 1)
            custom_author_font = custom_author_style.font
            custom_author_font.name = FONT_NAME
            custom_author_font.size = Pt(18)
            custom_author_font.color.rgb = RGBColor(80, 80, 80)
            custom_author_paragraph_format = (
                custom_author_style.paragraph_format
            )
            custom_author_paragraph_format.space_before = Pt(12)
            custom_author_paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Create a custom style for the date
        if "Custom Title Date" not in doc.styles:
            custom_date_style = doc.styles.add_style("Custom Title Date", 1)
            custom_date_font = custom_date_style.font
            custom_date_font.name = FONT_NAME
            custom_date_font.size = Pt(14)
            custom_date_font.color.rgb = RGBColor(80, 80, 80)
            custom_date_paragraph_format = custom_date_style.paragraph_format
            custom_date_paragraph_format.space_before = Pt(6)
            custom_date_paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

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
        self.set_style(doc)

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
