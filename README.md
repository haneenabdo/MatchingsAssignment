# MatchingsAssignment

## Students

-**Haneen Abdo** - UFID:66056936
-**Carson Reis** - UFID:

## Project Overview

This project implements the hospital-proposing Gale–Shapley deferred acceptance algorithm for a one-to-one hospital–student matching market. It also includes a verifier that checks whether a proposed matching is both valid and stable, as well as a scalability analysis measuring the runtime of both the matcher and the verifier for increasing input sizes.

## Repository Structure
src/
  main.py
  matcher.py
  verifier.py
  parser.py
  models.py
tests/
  test_matcher.py
  test_parser.py
  test_verifier.py
data/
  example.in
  example.out

## Requirements / Dependencies

- Python **3.9 or higher**

No external libraries are required. All functionality is implemented using Python’s standard library.

## Input Format

First line: integer n (number of hospitals and students)
Next n lines: hospital preference lists (permutations of 1..n)
Next n lines: student preference lists (permutations of 1..n)

Example (data/example.in):
3
1 2 3
2 3 1
2 1 3
2 1 3
1 2 3
1 2 3

## Output Format (Matcher)

The matcher outputs n lines, one per hospital:
i j
meaning hospital i is matched to student j.

Example (data/example.out):
1 1
2 2
3 3

## How to run the Matcher (Task A)

**From the repository root:**

PYTHONPATH=src python3 src/main.py match data/example.in

**To save the matching to a file:**

PYTHONPATH=src python3 src/main.py match data/example.in > outputs/match.out

The matcher prints the matching to stdout. The number of proposals is printed to stderr.

## How to run the Verifier (Task B)

The verifier checks:

Validity: each hospital and student is matched exactly once

Stability: no blocking pair exists

**Run:**

PYTHONPATH=src python3 src/main.py verify data/example.in --matching data/example.out

Possible outputs: VALID STABLE, INVALID (reason), UNSTABLE (blocking pair: hospital i, student j)

## Running Unit Tests

**Individual test files can be run with:**
PYTHONPATH=src python3 -m unittest tests/test_matcher.py
PYTHONPATH=src python3 -m unittest tests/test_parser.py
PYTHONPATH=src python3 -m unittest tests/test_verifier.py

## Scalability Analysis

We measured the runtime of:

The matcher (gale_shapley)

The verifier (validity + stability checks)

For input sizes:

n = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512

Each experiment was repeated multiple times and averaged to reduce noise.
Synthetic instances with complete preference lists were generated for each n.

## Matcher Runtime Results

Graph: matcher_runtime.png
Observed trend:
The matcher runtime increases superlinearly, consistent with the Gale–Shapley algorithm’s O(n²) worst-case number of proposals. In our implementation, each iteration scans for a free hospital, adding extra overhead and causing a steeper increase for larger n.

## Verifier Runtime Results

Graph: outputs/verifier_runtime.png
Observed trend:
The verifier runtime is nearly constant for small n, where Python overhead dominates. For larger n, runtime grows rapidly, reflecting the verifier’s O(n²) complexity due to rank table construction and exhaustive blocking-pair checks.

## Comparison

For large inputs, the verifier is slower than the matcher because it explicitly checks all hospital–student pairs, while the matcher processes proposals incrementally.

## Assumptions

-Input rankings are complete and strict permutations of 1..n

-Number of hospitals equals number of students

-Python runtime overhead affects small-n measurements

-Matcher output format strictly follows i j per line