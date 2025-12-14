#!/usr/bin/python3
"""Minimal Markdown to HTML converter entrypoint."""


import os
import sys
import re
import hashlib


def process_inline_formatting(text):
    """
    Process inline markdown formatting:
    **bold**, __italic__, [[MD5]], ((remove c)).
    """
    def md5_replace(match):
        content = match.group(1)
        md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        return md5_hash

    text = re.sub(r'\[\[(.+?)\]\]', md5_replace, text)

    def remove_c_replace(match):
        content = match.group(1)
        return content.translate(str.maketrans('', '', 'cC'))

    text = re.sub(r'\(\((.+?)\)\)', remove_c_replace, text)


    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def main():
    """
    Validate arguments and prepare output file.
    """
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
        list_type = None
        paragraph_lines = []

        def output_paragraph():
            """
            Output collected paragraph lines as HTML.
            """
            nonlocal paragraph_lines
            if paragraph_lines:
                f_out.write("<p>\n")
                f_out.write(process_inline_formatting(paragraph_lines[0]))
                for para_line in paragraph_lines[1:]:
                    f_out.write("<br/>\n")
                    f_out.write(process_inline_formatting(para_line))
                f_out.write("</p>\n")
                paragraph_lines = []

        for line in f_md:
            stripped = line.rstrip("\n")


            if stripped.startswith("#"):
                hashes, _, text = stripped.partition(" ")
                level = len(hashes)
                if 1 <= level <= 6 and text:
                    output_paragraph()
                    if in_list:
                        f_out.write(f"</{list_type}>\n")
                        in_list = False
                        list_type = None
                    formatted_text = process_inline_formatting(text)
                    f_out.write(f"<h{level}>{formatted_text}</h{level}>\n")
                    continue


            if stripped.startswith("* "):
                output_paragraph()
                if not in_list:
                    f_out.write("<ol>\n")
                    in_list = True
                    list_type = "ol"
                item_text = stripped[2:]
                formatted_text = process_inline_formatting(item_text)
                f_out.write(f"<li>{formatted_text}</li>\n")
                continue


            if stripped.startswith("- "):
                output_paragraph()
                if not in_list:
                    f_out.write("<ul>\n")
                    in_list = True
                    list_type = "ul"
                item_text = stripped[2:]
                formatted_text = process_inline_formatting(item_text)
                f_out.write(f"<li>{formatted_text}</li>\n")
                continue


            if in_list:
                f_out.write(f"</{list_type}>\n")
                in_list = False
                list_type = None


            if not stripped:
                output_paragraph()
                continue


            paragraph_lines.append(stripped)


        output_paragraph()
        if in_list:
            f_out.write(f"</{list_type}>\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
