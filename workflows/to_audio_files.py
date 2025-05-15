import os
import sys

from utils import Log

from convert import MarkdownDoc

log = Log("md_from_dir")


def main(md_file_path, max_words_per_part):
    log.debug(f"{md_file_path=}, {max_words_per_part=}")
    assert md_file_path.endswith(".md"), f"{md_file_path} is not a .md file"
    assert os.path.exists(md_file_path), f"{md_file_path} does not exist"

    doc = MarkdownDoc.from_file(md_file_path)
    doc.to_audio_files(md_file_path + ".audio", max_words_per_part)


if __name__ == "__main__":
    md_file_path = sys.argv[1]
    max_words_per_part = int(sys.argv[2])
    main(md_file_path, max_words_per_part)
