import os

from utils import Log

from convert.core import DocXDoc, MarkdownDirDoc, MarkdownDoc

log = Log("Convert")


class Convert:
    @staticmethod
    def get_doc_cls(file_or_dir_path: str):
        if file_or_dir_path.endswith(".docx"):
            return DocXDoc

        if file_or_dir_path.endswith(".md"):
            return MarkdownDoc

        if file_or_dir_path.endswith(".md.dir"):
            return MarkdownDirDoc

        raise ValueError(f"Invalid file_or_dir_path: {file_or_dir_path}")

    @staticmethod
    def convert(source_path: str, dest_path: str) -> None:
        assert os.path.exists(source_path)

        source_cls = Convert.get_doc_cls(source_path)
        dest_cls = Convert.get_doc_cls(dest_path)

        doc = source_cls.from_file(source_path)
        dest_cls(doc.paragraphs).to_file(dest_path)

        log.info(f'Converted "{source_path}" to "{dest_path}"')
