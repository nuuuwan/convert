import os
import unittest

from convert import Convert


class TestCase(unittest.TestCase):
    source_file_paths = [
        os.path.join("tests", "examples-output", "test.docx"),
        os.path.join("tests", "examples-output", "test.md"),
        os.path.join("tests", "examples-output", "test.md.dir"),
    ]
    dest_file_paths = [
        os.path.join("tests", "examples-output", "test2.docx"),
        os.path.join("tests", "examples-output", "test2.md"),
        os.path.join("tests", "examples-output", "test2.md.dir"),
    ]

    for source_file_path in source_file_paths:
        for dest_file_path in dest_file_paths:
            Convert.convert(
                source_path=source_file_path,
                dest_path=dest_file_path,
            )
