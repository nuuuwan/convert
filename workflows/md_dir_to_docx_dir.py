import os
import sys

from utils import Log

from convert import DocXDoc, MarkdownDoc

log = Log("docx_to_md")


def md_to_docx(md_path, docx_path):
    md_doc = MarkdownDoc.from_file(md_path)
    docx_doc = DocXDoc.from_instance(md_doc)
    docx_doc.to_file(docx_path)


def main(md_dir_path):
    assert md_dir_path.endswith("_md")
    assert os.path.exists(md_dir_path)

    docx_dir_path = md_dir_path[:-3] + "_docx"
    assert not os.path.exists(docx_dir_path)
    os.makedirs(docx_dir_path)
    log.info(f"Created {docx_dir_path}")

    for md_filename in os.listdir(md_dir_path):
        assert md_filename.endswith(".md")
        md_path = os.path.join(md_dir_path, md_filename)
        docx_filename = md_filename[:-3] + ".docx"
        docx_path = os.path.join(docx_dir_path, docx_filename)
        md_to_docx(md_path, docx_path)

    log.debug(f"Converted {md_dir_path} -> {docx_dir_path}")


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
