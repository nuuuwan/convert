import os
import sys

from convert import DocXDoc, MarkdownDirDoc

"""
Testing
python workflows/docx_to_md_dir.py \
  tests/examples/test.docx tests/examples-output/test3_md_dir
"""


def main(docx_path: str, md_dir_path: str) -> None:
    assert docx_path.endswith(".docx")
    assert not os.path.exists(md_dir_path) or os.path.isdir(md_dir_path)
    doc = DocXDoc.from_file(docx_path)
    MarkdownDirDoc(doc.paragraphs).to_file(md_dir_path)


if __name__ == "__main__":
    main(docx_path=sys.argv[1], md_dir_path=sys.argv[2])
