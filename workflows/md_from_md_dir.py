import os
import sys

from utils import Log

from convert import DocXDoc, MarkdownDoc, TexDoc

log = Log("md_from_dir")


def main(dir_path):
    doc = MarkdownDoc.from_dir(dir_path)
    doc.to_file(os.path.join(dir_path + ".all.md"))

    TexDoc.from_instance(doc).to_file(os.path.join(dir_path + ".all.tex"))

    parent_dir_path = os.path.dirname(dir_path)
    os.startfile(parent_dir_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
