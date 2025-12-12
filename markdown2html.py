#!/usr/bin/python3
import sys
import os

if __name__ == "__main__":

    # Check number of arguments (requires EXACTLY 2 arguments after script name)
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if Markdown file exists
    if not os.path.isfile(md_file):
        print("Missing {}".format(md_file), file=sys.stderr)
        sys.exit(1)

    # If everything is good → print nothing and exit 0
    sys.exit(0)
