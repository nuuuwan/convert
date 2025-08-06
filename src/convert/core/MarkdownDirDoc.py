import os

from utils import Log

from convert.core.AbstractDoc import AbstractDoc
from convert.core.MarkdownDoc import MarkdownDoc
from convert.core.Paragraph import Paragraph

log = Log("MarkdownDirDoc")


class MarkdownDirDoc(AbstractDoc):
    """
    Current implementation: Single level.
    H1 has dir. Each H2 has a file with that H2 as the first header.
    """

    @classmethod
    def __gen_dir_h1_name_and_paths__(cls, file_path):
        assert os.path.isdir(file_path)
        for dir_h1_name in sorted(os.listdir(file_path)):
            dir_h1_path = os.path.join(file_path, dir_h1_name)
            if not os.path.isdir(dir_h1_path):
                continue
            if dir_h1_name.startswith("."):
                continue
            yield dir_h1_name, dir_h1_path

    @classmethod
    def from_file(cls, file_path: str) -> "MarkdownDirDoc":
        paragraphs = []
        for dir_h1_name, dir_h1_path in cls.__gen_dir_h1_name_and_paths__(
            file_path
        ):
            paragraphs.append(Paragraph("h1", dir_h1_name))
            for file_name in sorted(os.listdir(dir_h1_path)):
                if not file_name.endswith(".md"):
                    continue
                md_path = os.path.join(dir_h1_path, file_name)
                md_doc = MarkdownDoc.from_file(md_path).level_down()
                paragraphs.extend(md_doc.paragraphs)

        doc = cls(paragraphs)
        doc.clean()
        return doc

    def __h1_to_h2_to_paragraphs__(self):
        idx = {}
        cur_h1 = None
        cur_h2 = None
        for paragraph in self.paragraphs:
            if paragraph.tag == "h1":
                idx[paragraph.text] = {}
                cur_h1 = paragraph.text
            elif paragraph.tag == "h2":
                assert cur_h1
                idx[cur_h1][paragraph.text] = [paragraph]
                cur_h2 = paragraph.text
            else:
                if cur_h1 and cur_h2:
                    idx[cur_h1][cur_h2].append(paragraph)
                else:
                    log.warning(f'No headings. Skipping "{paragraph.text}".')

        return idx

    def to_file(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        idx = self.__h1_to_h2_to_paragraphs__()
        for h1_name, h2_dict in idx.items():
            h1_path = os.path.join(file_path, h1_name)
            if not os.path.exists(h1_path):
                os.makedirs(h1_path, exist_ok=True)
            for h2_name, paragraphs in h2_dict.items():
                md_path = os.path.join(h1_path, f"{h2_name}.md")
                MarkdownDoc(paragraphs).level_up().to_file(md_path)

        log.info(f"Wrote {file_path}")
