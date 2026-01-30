# types.py
#
# Shared data structures used across the project.
# Both matcher and verifier need to work with the same shape of parsed input

from dataclasses import dataclass
from typing import List

PrefList = List[int]
Prefs = List[PrefList]

@dataclass(frozen=True)
class ProblemInstance:
    # Number of hospitals and the number of students (must be equal)
    n: int

    # hospital_prefs[h] is the preference list for hospital (h + 1)
    hospital_prefs: Prefs

    # student_prefs[s] is the preference list for student (s + 1)
    student_prefs: Prefs
