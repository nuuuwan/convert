import os
import sys

from utils import Log

from convert import DocXDoc, MarkdownDoc

log = Log("docx_to_md")


def docx_to_md(docx_path, md_path):
    docx_doc = DocXDoc.from_file(docx_path)
    md_doc = MarkdownDoc.from_instance(docx_doc)
    md_doc.to_file(md_path)
    log.debug(f"Converted {docx_path} -> {md_path}")


def main(dir_path):
    dir_path_md = dir_path + ".md"
    os.makedirs(dir_path_md, exist_ok=True)
    log.info(f"Created {dir_path_md}")

    for filename in os.listdir(dir_path):
        if filename.endswith(".docx"):
            docx_path = os.path.join(dir_path, filename)
            md_path = os.path.join(
                dir_path_md, filename.replace(".docx", ".md")
            )
            docx_to_md(docx_path, md_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
