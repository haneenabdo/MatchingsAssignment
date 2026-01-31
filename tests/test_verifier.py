import os
import unittest
import tempfile
from io import StringIO

from parser import parse_instance
from verifier import verify_instance


class TestVerifier(unittest.TestCase):
    def _write_temp_matching(self, lines):
        """
        Helper: write matching lines to a temp file and return its path.
        lines: list[str] like ["1 1", "2 2", ...]
        """
        fd, path = tempfile.mkstemp(prefix="matching_", suffix=".out", text=True)
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            for ln in lines:
                f.write(ln.rstrip() + "\n")
        return path

    def test_valid_stable_from_string(self):
        s = """3
        1 2 3
        2 3 1
        2 1 3
        2 1 3
        1 2 3
        1 2 3
        """
        inst = parse_instance(StringIO(s))

        # stable matching for this instance
        match_path = self._write_temp_matching([
            "1 1",
            "2 2",
            "3 3",
        ])

        try:
            ok_valid, ok_stable, msg = verify_instance(inst, match_path)
            self.assertTrue(ok_valid)
            self.assertTrue(ok_stable)
            self.assertEqual(msg, "VALID STABLE")
        finally:
            os.remove(match_path)

    def test_invalid_duplicate_student(self):
        s = """3
        1 2 3
        2 3 1
        2 1 3
        2 1 3
        1 2 3
        1 2 3
        """
        inst = parse_instance(StringIO(s))

        # student 1 matched twice
        match_path = self._write_temp_matching([
            "1 1",
            "2 1",
            "3 2",
        ])

        try:
            ok_valid, ok_stable, msg = verify_instance(inst, match_path)
            self.assertFalse(ok_valid)
            self.assertIn("INVALID", msg)
        finally:
            os.remove(match_path)

    def test_invalid_out_of_range(self):
        s = """3
        1 2 3
        2 3 1
        2 1 3
        2 1 3
        1 2 3
        1 2 3
        """
        inst = parse_instance(StringIO(s))

        # student id 4 out of range (n=3)
        match_path = self._write_temp_matching([
            "1 4",
            "2 2",
            "3 3",
        ])

        try:
            ok_valid, ok_stable, msg = verify_instance(inst, match_path)
            self.assertFalse(ok_valid)
            self.assertIn("INVALID", msg)
        finally:
            os.remove(match_path)

    def test_unstable_blocking_pair(self):
        s = """2
        1 2
        1 2
        1 2
        1 2
        """
        inst = parse_instance(StringIO(s))

        # Matching: H1->S2, H2->S1 is unstable because (H1,S1) blocks
        match_path = self._write_temp_matching([
            "1 2",
            "2 1",
        ])

        try:
            ok_valid, ok_stable, msg = verify_instance(inst, match_path)
            self.assertTrue(ok_valid)
            self.assertFalse(ok_stable)
            self.assertIn("UNSTABLE", msg)
            self.assertIn("hospital 1", msg)
            self.assertIn("student 1", msg)
        finally:
            os.remove(match_path)

    def test_valid_example_file_in_repo(self):
        # uses your repo file data/example.in
        here = os.path.dirname(__file__)
        prefs_path = os.path.abspath(os.path.join(here, "..", "data", "example.in"))

        with open(prefs_path, "r", encoding="utf-8") as f:
            inst = parse_instance(f)

        match_path = os.path.abspath(os.path.join(here, "..", "data", "example.out"))

        ok_valid, ok_stable, msg = verify_instance(inst, match_path)
        self.assertTrue(ok_valid)
        self.assertTrue(ok_stable)
        self.assertEqual(msg, "VALID STABLE")


if __name__ == "__main__":
    unittest.main()
