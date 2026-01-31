import os
import unittest
from io import StringIO

from parser import parse_instance, ParseError


class TestParser(unittest.TestCase):
    def test_valid(self):
        s = """3
        1 2 3
        2 3 1
        2 1 3
        2 1 3
        1 2 3
        1 2 3
        """
        inst = parse_instance(StringIO(s))
        self.assertEqual(inst.n, 3)

        # basic shape checks, n hospital lines and n student lines
        self.assertEqual(len(inst.hospital_prefs), 3)
        self.assertEqual(len(inst.student_prefs), 3)

        # check a row length and a first preference
        self.assertEqual(len(inst.hospital_prefs[0]), 3)
        self.assertEqual(inst.hospital_prefs[0][0], 1)
        self.assertEqual(len(inst.student_prefs[0]), 3)
        self.assertEqual(inst.student_prefs[0][0], 2)

    def test_empty(self):
        with self.assertRaises(ParseError):
            parse_instance(StringIO(""))

    def test_wrong_count(self):
        s = """2
        1 2
        2 1
        1 2
        """  # missing one student line
        with self.assertRaises(ParseError):
            parse_instance(StringIO(s))

    def test_duplicate(self):
        s = """2
        1 1
        2 1
        1 2
        2 1
        """
        with self.assertRaises(ParseError):
            parse_instance(StringIO(s))

    def test_valid_example_file(self):
        here = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(here, "..", "data", "example.in"))

        with open(path, "r", encoding="utf-8") as f:
            inst = parse_instance(f)

        self.assertEqual(inst.n, 3)


if __name__ == "__main__":
    unittest.main()

