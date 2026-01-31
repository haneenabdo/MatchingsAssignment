from __future__ import annotations

import argparse
from typing import List, Tuple, Optional


def read_preference_lines(path: str) -> Tuple[Optional[Tuple[int, List[List[int]], List[List[int]]]], Optional[str]]:
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read().strip()

    if txt == "":
        return None, "Empty input file."

    tokens = txt.split()
    try:
        n = int(tokens[0])
    except Exception:
        return None, "First line is not an integer."

    if n < 0:
        return None, "n must be non-negative."

    idx = 1
    if n == 0:
        if idx != len(tokens):
            return None, "Input should end after 0, but more values were provided."
        return (0, [], []), None

    def read_group_block(group: str) -> List[List[int]]:
        nonlocal idx
        block: List[List[int]] = []
        for line_i in range(n):
            if idx + n > len(tokens):
                raise ValueError(f"Not enough integers for {group} preferences.")
            row = list(map(int, tokens[idx: idx + n]))
            idx += n

            if sorted(row) != list(range(1, n + 1)):
                raise ValueError(f"{group} line {line_i + 1} is not a permutation of 1..{n}.")

            block.append([x - 1 for x in row])
        return block

    try:
        hospital_prefs = read_group_block("Hospital")
        applicant_prefs = read_group_block("Applicant") 
    except ValueError as e:
        return None, str(e)

    if idx != len(tokens):
        return None, "Extra tokens found after preferences."

    return (n, hospital_prefs, applicant_prefs), None


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
            applicant_id = int(parts[1])
        except Exception:
            return None, f"Line {k} contains non-integers."

        h = hospital_id - 1
        a = applicant_id - 1

        if not (0 <= h < n):
            return None, f"Hospital id {hospital_id} is out of range."
        if not (0 <= a < n):
            return None, f"Applicant id {applicant_id} is out of range."
        if hospital_seen[h]:
            return None, f"Hospital {hospital_id} appears multiple times."

        hospital_seen[h] = True
        match[h] = a

    # ensure all hospitals matched
    if any(x == -1 for x in match):
        return None, "Some hospitals are unmatched."

    return match, None


def main() -> None:
    ap = argparse.ArgumentParser(description="Verifier for hospital-student matching.")
    ap.add_argument("--prefs", required=True, help="Preferences file in assignment format.")
    ap.add_argument("--matching", required=True, help="Matching file with n lines of 'i j'.")
    args = ap.parse_args()

    parsed, err = read_preference_lines(args.prefs)
    if err:
        print(f"INVALID ({err})")
        return

    n, hospital_prefs, applicant_prefs = parsed

    match, err = read_matching(args.matching, n)
    if err:
        print(f"INVALID ({err})")
        return

    if n == 0:
        print("VALID STABLE")
        return

    applicant_seen = [False] * n
    for h in range(n):
        a = match[h]
        if applicant_seen[a]:
            print(f"INVALID (Applicant {a + 1} matched to multiple hospitals.)")
            return
        applicant_seen[a] = True

    if not all(applicant_seen):
        print("INVALID (Some applicants are unmatched.)")
        return

    rank_h = [[0] * n for _ in range(n)]
    for h in range(n):
        for pos, a in enumerate(hospital_prefs[h]):
            rank_h[h][a] = pos

    rank_a = [[0] * n for _ in range(n)]
    for a in range(n):
        for pos, h in enumerate(applicant_prefs[a]):
            rank_a[a][h] = pos

    partner_of_applicant = [-1] * n
    for h in range(n):
        partner_of_applicant[match[h]] = h

    for h in range(n):
        a_current = match[h]
        for a in range(n):
            if a == a_current:
                continue

            h_current = partner_of_applicant[a]

            if (rank_h[h][a] < rank_h[h][a_current] and
                rank_a[a][h] < rank_a[a][h_current]):
                print(f"UNSTABLE (blocking pair: hospital {h + 1}, applicant {a + 1})")
                return

    print("VALID STABLE")


if __name__ == "__main__":
    main()
