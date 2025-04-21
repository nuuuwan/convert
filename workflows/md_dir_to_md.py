import os
import sys

from utils import Log

from convert import MarkdownDoc

log = Log("md_from_dir")


def main(dir_path):
    doc = MarkdownDoc.from_dir(dir_path)
    doc.to_file(os.path.join(dir_path + ".all.md"))


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
