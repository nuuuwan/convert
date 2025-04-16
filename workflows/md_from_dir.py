import os
import sys

from utils import Log

from convert import DocXDoc, MarkdownDoc, TexDoc

log = Log("md_from_dir")


def main(dir_path, title):
    doc = MarkdownDoc.from_dir(dir_path, title)
    doc.to_file(os.path.join(dir_path + ".all.md"))

    TexDoc.from_instance(doc).to_file(os.path.join(dir_path + ".all.tex"))
    DocXDoc.from_instance(doc).to_file(os.path.join(dir_path + ".all.docx"))

    os.startfile(dir_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    title = sys.argv[2]
    main(dir_path, title)
