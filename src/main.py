import sys
import argparse

from parser import parse_instance, ParseError
from matcher import gale_shapley



def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python main.py",
        description="Parse an instance file and run either matching or verification.",
    )


    p.add_argument(
        "mode",
        choices=("match", "verify"),
        help="operation mode (expected: match|verify)",
    )

    p.add_argument(
        "input_file",
        nargs="?",
        default="-",
        help="path to input file, or '-' to read from stdin (default: '-')",
    )

    p.add_argument(
        "--validate-only",
        action="store_true",
        help="only validate that the input parses; don't do any work",
    )

    return p


def load_instance(input_path: str):

    try:
        if input_path == "-":
            return parse_instance(sys.stdin)
        # utf-8 explicitly stated should make parsing more consistent across platforms
        with open(input_path, "r", encoding="utf-8") as f:
            return parse_instance(f)
    except FileNotFoundError:
        print(f"invalid input: no such file: {input_path}", file=sys.stderr)
        return None
    except ParseError as e:
        print(f"invalid input: {e}", file=sys.stderr)
        return None


def main() -> int:

    parser = build_parser()

    ns = parser.parse_args()

    instance = load_instance(ns.input_file)

    if instance is None:
        return 1

    if ns.validate_only:
        return 0

    # TODO: matcher and verifier and write results to stdout, stderr = logs

    print(f"ok (parsed n={instance.n})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
