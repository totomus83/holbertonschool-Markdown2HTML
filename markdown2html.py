#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML (initial version).
Handles only argument validation for now.
"""

import sys
import os

def main():
    # Check the number of arguments (script name is argv[0])
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        sys.exit(1)

    # If everything is fine, do nothing and exit 0
    sys.exit(0)


if __name__ == "__main__":
    main()
