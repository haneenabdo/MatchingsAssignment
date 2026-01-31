from __future__ import annotations
from typing import List, Tuple, Optional
from models import ProblemInstance

def read_matching(path: str, n: int) -> Tuple[Optional[List[int]], Optional[str]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip() != ""]

    if n == 0:
        if len(lines) != 0:
            return None, "n=0 but matching file is not empty as expected."
        return [], None

    if len(lines) != n:
        return None, f"Matching must have exactly {n} non-empty lines."

    match = [-1] * n
    hospital_seen = [False] * n

    for k, ln in enumerate(lines, start=1):
        parts = ln.split()
        if len(parts) != 2:
            return None, f"Line {k} must contain exactly 2 integers."

        try:
            hospital_id = int(parts[0])
            student_id = int(parts[1])
        except Exception:
            return None, f"Line {k} contains non-integers."

        h = hospital_id - 1
        s = student_id - 1

        if not (0 <= h < n):
            return None, f"Hospital id {hospital_id} is out of range."
        if not (0 <= s < n):
            return None, f"Student id {student_id} is out of range."
        if hospital_seen[h]:
            return None, f"Hospital {hospital_id} appears multiple times."

        hospital_seen[h] = True
        match[h] = s

    if any(x == -1 for x in match):
        return None, "Some hospitals are unmatched."

    return match, None


def verify_instance(instance: ProblemInstance, matching_path: str) -> Tuple[bool, bool, str]:
    """
    Returns (is_valid, is_stable, message)
    message is one of:
      VALID STABLE
      INVALID (...)
      UNSTABLE (blocking pair: hospital i, student j)
    """
    n = instance.n
    match, err = read_matching(matching_path, n)
    if err:
        return False, False, f"INVALID ({err})"

    if n == 0:
        return True, True, "VALID STABLE"

    # Validity: each student exactly once
    student_seen = [False] * n
    for h in range(n):
        s = match[h]
        if student_seen[s]:
            return False, False, f"INVALID: Student {s + 1} matched to multiple hospitals."
        student_seen[s] = True

    if not all(student_seen):
        return False, False, "INVALID: Some students are unmatched."

    hosp_prefs = instance.hospital_prefs
    stud_prefs = instance.student_prefs

    # Build rank tables
    rank_h = [[0] * n for _ in range(n)]
    for h in range(n):
        for pos, s_id in enumerate(hosp_prefs[h]):
            rank_h[h][s_id - 1] = pos  # convert to 0-based student index

    rank_s = [[0] * n for _ in range(n)]
    for s in range(n):
        for pos, h_id in enumerate(stud_prefs[s]):
            rank_s[s][h_id - 1] = pos  # convert to 0-based hospital index

    # Invert matching: partner_of_student[s] = h
    partner_of_student = [-1] * n
    for h in range(n):
        partner_of_student[match[h]] = h

    # Stability: find blocking pair
    for h in range(n):
        s_current = match[h]
        for s in range(n):
            if s == s_current:
                continue
            h_current = partner_of_student[s]

            if (rank_h[h][s] < rank_h[h][s_current] and
                rank_s[s][h] < rank_s[s][h_current]):
                return True, False, f"UNSTABLE: blocking pair: hospital {h + 1}, student {s + 1}"

    return True, True, "VALID STABLE"
