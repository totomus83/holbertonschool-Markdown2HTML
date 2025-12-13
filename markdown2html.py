#!/usr/bin/python3
"""Minimal Markdown to HTML converter entrypoint."""


import os
import sys


def main():
    """Validate arguments and prepare output file."""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    with open(md_file, "r", encoding="utf-8") as f_md, open(
        output_file, "w", encoding="utf-8"
    ) as f_out:
        in_list = False

        for line in f_md:
            stripped = line.rstrip("\n")

            # Headings
            if stripped.startswith("#"):
                hashes, _, text = stripped.partition(" ")
                level = len(hashes)
                if 1 <= level <= 6 and text:
                    if in_list:
                        f_out.write("</ul>\n")
                        in_list = False
                    f_out.write(f"<h{level}>{text}</h{level}>\n")
                    continue

            if stripped.startswith("- "):
                if not in_list:
                    f_out.write("<ul>\n")
                    in_list = True
                item_text = stripped[2:]
                f_out.write(f"<li>{item_text}</li>\n")
                continue

            if in_list:
                f_out.write("</ul>\n")
                in_list = False

            if line.endswith("\n"):
                f_out.write(stripped + "\n")
            else:
                f_out.write(stripped)

        if in_list:
            f_out.write("</ul>\n")

    sys.exit(0)


if __name__ == "__main__":
    main()