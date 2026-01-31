import os
import time
import csv
import subprocess

import matplotlib.pyplot as plt


NS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
REPEATS = 5  # average runs to reduce noise

OUT_DIR = "outputs"
TMP_PREFS = os.path.join(OUT_DIR, "tmp_prefs.in")
TMP_MATCH = os.path.join(OUT_DIR, "tmp_match.out")
CSV_PATH = os.path.join(OUT_DIR, "verifier_times.csv")
PLOT_PATH = os.path.join(OUT_DIR, "verifier_runtime.png")


def write_easy_stable_instance(n: int, prefs_path: str, match_path: str):
    """
    Create preferences where everyone ranks 1..n in order.
    Identity matching i->i is then stable (everyone gets top choice).
    """
    with open(prefs_path, "w", encoding="utf-8") as f:
        f.write(str(n) + "\n")
        # hospitals
        for _ in range(n):
            f.write(" ".join(str(x) for x in range(1, n + 1)) + "\n")
        # applicants/students
        for _ in range(n):
            f.write(" ".join(str(x) for x in range(1, n + 1)) + "\n")

    with open(match_path, "w", encoding="utf-8") as f:
        for i in range(1, n + 1):
            f.write(f"{i} {i}\n")


def time_verifier_once(prefs_path: str, match_path: str) -> float:
    t0 = time.perf_counter()
    p = subprocess.run(
        ["python3", "verifier.py", "--prefs", prefs_path, "--matching", match_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    t1 = time.perf_counter()

    # Safety: if verifier crashes, show output and stop
    if p.returncode not in (0, 1, 2):
        raise RuntimeError(f"Verifier crashed.\nSTDERR:\n{p.stderr}\nSTDOUT:\n{p.stdout}")

    return t1 - t0


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    xs = []
    ys = []

    for n in NS:
        write_easy_stable_instance(n, TMP_PREFS, TMP_MATCH)

        total = 0.0
        for _ in range(REPEATS):
            total += time_verifier_once(TMP_PREFS, TMP_MATCH)
        avg = total / REPEATS

        xs.append(n)
        ys.append(avg)
        print(f"n={n}: verifier avg time = {avg:.6f} seconds")

    # Save CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "avg_time_seconds"])
        w.writerows(zip(xs, ys))

    # Plot line graph
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.xlabel("n (hospitals/students)")
    plt.ylabel("Average time (seconds)")
    plt.title("Verifier runtime vs n")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=200)
    plt.close()

    print(f"\nSaved: {CSV_PATH}")
    print(f"Saved: {PLOT_PATH}")


if __name__ == "__main__":
    main()
