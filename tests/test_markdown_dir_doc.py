import unittest

from convert import MarkdownDirDoc
from tests.common_test import helper_test_rotation


class TestCase(unittest.TestCase):

    def test_rotation(self):
        helper_test_rotation(self, MarkdownDirDoc, "test.md.dir")
