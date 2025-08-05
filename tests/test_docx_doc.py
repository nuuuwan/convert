import unittest

from convert import DocXDoc
from tests.common_test import helper_test_rotation


class TestCase(unittest.TestCase):
    def test_rotation(self):
        helper_test_rotation(self, DocXDoc, "test.docx")
