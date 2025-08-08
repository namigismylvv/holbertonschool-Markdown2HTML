#!/usr/bin/python3
"""
Markdown to HTML converter — hash,remove a letter
"""

import sys
import os
import re
import hashlib

def parse_special(text):
    def md5_replace(match):
        content = match.group(1)
        md5hash = hashlib.md5(content.encode()).hexdigest()
        return md5hash

    text = re.sub(r"\[\[(.+?)\]\]", md5_replace, text)

    def remove_c_replace(match):
        content = match.group(1)
        return re.sub(r"[cC]", "", content)

    text = re.sub(r"\(\((.+?)\)\)", remove_c_replace, text)

    return text

def parse_bold_italic(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<em>\1</em>", text)
    return text

def parse_line(text):
    text = parse_special(text)
    text = parse_bold_italic(text)
    return text

def markdown_to_html(text):
    html_lines = []
    in_ul = False
    in_ol = False
    in_paragraph = False
    paragraph_lines = []

    for line in text.split('\n'):
        stripped = line.strip()

        if stripped.startswith('#'):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_paragraph:
                paragraph_lines = [parse_line(l) for l in paragraph_lines]
                html_lines.append("<p>")
                html_lines.extend(
                    paragraph_lines[0:1] +
                    [f"<br/>{l}" for l in paragraph_lines[1:]]
                )
                html_lines.append("</p>")
                paragraph_lines = []
                in_paragraph = False

            count = 0
            for char in stripped:
                if char == '#':
                    count += 1
                else:
                    break
            content = stripped[count:].strip()
            content = parse_line(content)
            html_lines.append(f"<h{count}>{content}</h{count}>")

        elif stripped.startswith('- '):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_paragraph:
                paragraph_lines = [parse_line(l) for l in paragraph_lines]
                html_lines.append("<p>")
                html_lines.extend(
                    paragraph_lines[0:1] +
                    [f"<br/>{l}" for l in paragraph_lines[1:]]
                )
                html_lines.append("</p>")
                paragraph_lines = []
                in_paragraph = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = stripped[2:].strip()
            content = parse_line(content)
            html_lines.append(f"<li>{content}</li>")

        elif stripped.startswith('* '):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_paragraph:
                paragraph_lines = [parse_line(l) for l in paragraph_lines]
                html_lines.append("<p>")
                html_lines.extend(
                    paragraph_lines[0:1] +
                    [f"<br/>{l}" for l in paragraph_lines[1:]]
                )
                html_lines.append("</p>")
                paragraph_lines = []
                in_paragraph = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = stripped[2:].strip()
            content = parse_line(content)
            html_lines.append(f"<li>{content}</li>")

        elif stripped == '':
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_paragraph:
                paragraph_lines = [parse_line(l) for l in paragraph_lines]
                html_lines.append("<p>")
                html_lines.extend(
                    paragraph_lines[0:1] +
                    [f"<br/>{l}" for l in paragraph_lines[1:]]
                )
                html_lines.append("</p>")
                paragraph_lines = []
                in_paragraph = False

        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False

            in_paragraph = True
            paragraph_lines.append(stripped)

    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")
    if in_paragraph:
        paragraph_lines = [parse_line(l) for l in paragraph_lines]
        html_lines.append("<p>")
        html_lines.extend(
            paragraph_lines[0:1] +
            [f"<br/>{l}" for l in paragraph_lines[1:]]
        )
        html_lines.append("</p>")

    return '\n'.join(html_lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    with open(md_file, 'r') as f:
        md_content = f.read()

    html_content = markdown_to_html(md_content)

    with open(html_file, 'w') as f:
        f.write(html_content)

    sys.exit(0)


if __name__ == "__main__":
    main()

