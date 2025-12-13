#!/usr/bin/python3
"""
Write a script that takes an argument 2 strings
"""

import sys
import os


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]

    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
