#!/usr/bin/python3
"""
Markdown to HTML converter — headings + unordered and ordered lists
"""

import sys
import os

def markdown_to_html(text):
    html_lines = []
    in_ul = False   
    in_ol = False   

    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False

            count = 0
            for char in line:
                if char == '#':
                    count += 1
                else:
                    break
            content = line[count:].strip()
            html_lines.append(f"<h{count}>{content}</h{count}>")

        elif line.startswith('- '):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = line[2:].strip()
            html_lines.append(f"<li>{content}</li>")

        elif line.startswith('* '):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = line[2:].strip()
            html_lines.append(f"<li>{content}</li>")

        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False

    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

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
