import os
import sys
from convert import MarkdownDoc
from utils import Log

log = Log("md_from_dir")


def main(dir_path):
    MarkdownDoc.from_dir(dir_path).to_file(os.path.join(dir_path, "_all.md"))
    log.info(f"Created {os.path.join(dir_path, '_all.md')}")
    os.startfile(dir_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
