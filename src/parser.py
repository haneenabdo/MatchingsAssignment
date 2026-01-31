from typing import TextIO
from models import ProblemInstance

class ParseError(Exception):
    pass


def parse_instance(stream: TextIO) -> ProblemInstance:
    # read all non-empty lines, ignore blank lines
    # splitlines() removes trailing newline characters
    raw = stream.read().splitlines()

    lines = []
    for ln in raw:
        ln = ln.strip()
        if ln:
            lines.append(ln)

    if not lines:
        raise ParseError("empty input file")

    # the first non-empty line should contain only one integer, n
    # split done here to ensure it's not something incorrect like "3 4"
    first_parts = lines[0].split()
    if len(first_parts) != 1:
        raise ParseError("line 1: expected a single integer n")

    try:
        n = int(first_parts[0])
    except ValueError:
        raise ParseError("line 1: n must be an integer")


    if n < 0:
        raise ParseError("line 1: n must be >= 0")

    # after reading n, we know how many preference lines should exist,
    # 1 line for n. n lines for hospitals. n lines for students
    expected_lines = 1 + 2 * n
    if len(lines) != expected_lines:
        raise ParseError(f"expected {expected_lines} non-empty lines, found {len(lines)}")

    # helper func to validate single preference list
    # "nums" would be strict ranking of length n with no repeats and all vals in 1 to n
    def check_pref(nums, who, line_no):
        # each preference line must have exactly n integers, the entire ranking
        if len(nums) != n:
            raise ParseError(f"line {line_no}: {who} list must have {n} numbers")
        # set here to detect duplicates
        seen = set()

        # ensure each id is valid
        for x in nums:

            if x < 1 or x > n:
                raise ParseError(f"line {line_no}: {who} has out-of-range id {x}")

            if x in seen:
                raise ParseError(f"line {line_no}: {who} repeats id {x}")
            seen.add(x)

    hospital_prefs = []
    student_prefs = []

    # hospital preference lines
    for i in range(n):

        # line_no is line number within non-empty lines list (1-based)
        # matches the expected format- line 2 is hospital 1, line 3 is hospital 2....
        line_no = 2 + i
        parts = lines[1 + i].split()
        try:
            nums = [int(x) for x in parts]
        except ValueError:
            raise ParseError(f"line {line_no}: non-integer token found")

        check_pref(nums, f"hospital {i + 1}", line_no)
        hospital_prefs.append(nums)

    # student preference
    for i in range(n):

        # non-empty line number for this student preference line
        # line 2 + n is student 1, line 3 + n is student 2...
        line_no = 2 + n + i

        # split student preference line into tokens
        parts = lines[1 + n + i].split()

        # lastly, turn tokens to integers, throw error if no ints
        try:

            nums = [int(x) for x in parts]

        except ValueError:

            raise ParseError(f"line {line_no}: non-integer token found")

        check_pref(nums, f"student {i + 1}", line_no)
        student_prefs.append(nums)

    return ProblemInstance(n=n, hospital_prefs=hospital_prefs, student_prefs=student_prefs)
