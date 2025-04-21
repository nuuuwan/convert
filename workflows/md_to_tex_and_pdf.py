import sys

from utils import Log

from convert import MarkdownDoc, TexDoc

log = Log("md_from_dir")


def main(md_path):
    md_doc = MarkdownDoc.from_file(md_path)

    tex_path = md_path[:-3] + ".tex"
    tex_doc = TexDoc.from_instance(md_doc)
    tex_doc.to_file(tex_path)
    tex_doc.compile(tex_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
