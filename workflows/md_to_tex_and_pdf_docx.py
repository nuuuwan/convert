import sys
import os
from utils import Log

from convert import DocXDoc, MarkdownDoc, TexDoc

log = Log("md_from_dir")


def get_md_path(dir_path):
    assert os.path.exists(dir_path), f"{dir_path} does not exist"
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".md"):
            return os.path.join(dir_path, file_name)
    raise FileNotFoundError(f"No .md file found in {dir_path}")


def main(dir_path):
    md_path = get_md_path(dir_path)
    md_doc = MarkdownDoc.from_file(md_path)
    base_name = md_path[:-3]

    tex_path = base_name + ".tex"
    tex_doc = TexDoc.from_instance(md_doc)
    tex_doc.to_file(tex_path)
    tex_doc.compile(tex_path)

    docx_doc = DocXDoc.from_instance(md_doc)
    docx_path = base_name + ".docx"
    docx_doc.to_file(docx_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
