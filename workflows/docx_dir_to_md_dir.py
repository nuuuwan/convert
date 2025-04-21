import os
import sys

from utils import Log

from convert import DocXDoc, MarkdownDoc

log = Log("docx_to_md")


def docx_to_md(docx_path, md_path):
    assert docx_path.endswith(".docx"), f"docx_path: {docx_path}"
    assert md_path.endswith(".md"), f"md_path: {md_path}"
    assert os.path.exists(docx_path), f"{docx_path} does not exist"
    docx_doc = DocXDoc.from_file(docx_path)
    md_doc = MarkdownDoc.from_instance(docx_doc)
    md_doc.to_file(md_path)


def main(docx_dir_path):
    assert docx_dir_path.endswith("_docx"), f"docx_path: {docx_dir_path}"
    assert os.path.exists(docx_dir_path), f"{docx_dir_path} does not exist"

    md_dir_path = docx_dir_path[:-5] + "_md"
    assert not os.path.exists(md_dir_path), f"{md_dir_path} already exists"
    os.makedirs(md_dir_path)
    log.info(f"Created {md_dir_path}")

    for docx_filename in os.listdir(docx_dir_path):
        assert docx_filename.endswith(
            ".docx"
        ), f"docx_filename: {docx_filename}"
        docx_path = os.path.join(docx_dir_path, docx_filename)
        md_filename = docx_filename[:-5] + ".md"
        md_path = os.path.join(md_dir_path, md_filename)
        docx_to_md(docx_path, md_path)
    log.debug(f"Converted {docx_dir_path} -> {md_dir_path}")


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
