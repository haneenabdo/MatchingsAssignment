import unittest

from matcher import gale_shapley
from models import ProblemInstance


class TestMatcher(unittest.TestCase):

    def test_empty_instance(self):
        inst = ProblemInstance(
            n=0,
            hospital_prefs=[],
            student_prefs=[]
        )

        matches, proposals = gale_shapley(inst)

        self.assertEqual(matches, [])
        self.assertEqual(proposals, 0)

    def test_single_instance(self):
        inst = ProblemInstance(
            n=1,
            hospital_prefs=[[1]],
            student_prefs=[[1]]
        )

        matches, proposals = gale_shapley(inst)

        self.assertEqual(matches, [1])
        self.assertGreaterEqual(proposals, 1)

    def test_example_instance_valid_matching(self):
        inst = ProblemInstance(
            n=3,
            hospital_prefs=[
                [1, 2, 3],
                [2, 3, 1],
                [2, 1, 3],
            ],
            student_prefs=[
                [2, 1, 3],
                [1, 2, 3],
                [1, 2, 3],
            ],
        )

        matches, proposals = gale_shapley(inst)

        # correct size
        self.assertEqual(len(matches), 3)

        # every student appears exactly once
        self.assertEqual(set(matches), {1, 2, 3})

        # proposal count should be positive
        self.assertGreater(proposals, 0)


if __name__ == "__main__":
    unittest.main()
