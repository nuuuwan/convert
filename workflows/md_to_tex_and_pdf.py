import sys

from utils import Log

from convert import MarkdownDoc, TexDoc

log = Log("md_from_dir")


def main(md_path):
    doc = MarkdownDoc.from_file(md_path)
    tex_path = md_path[::-3] + ".tex"
    TexDoc.from_instance(doc).to_file(tex_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
