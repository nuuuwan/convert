import os
import sys

from utils import Log, TimeFormat, Time

from convert import MarkdownDoc

log = Log("md_from_dir")


def main(dir_path):
    doc = MarkdownDoc.from_dir(dir_path)
    parent_dir_path = os.path.dirname(dir_path)
    ts = TimeFormat.DATE_ID.format(Time.now())
    md_file_path = os.path.join(
        parent_dir_path, f"[NuwanS] The Lies They Told You.{ts}.md"
    )
    doc.to_file(md_file_path)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
