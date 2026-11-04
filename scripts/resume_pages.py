#!/usr/bin/env python3
"""Report page count and box warnings for compiled resume PDFs.

Used by .github/workflows/resume.yml. Reads the pdflatex .log files rather than
guessing from the PDF, so overfull/underfull boxes are surfaced explicitly.
"""
import pathlib
import re
import sys


def pages_from_log(log_text):
    """pdflatex prints: 'Output written on X.pdf (1 page, 12345 bytes).'"""
    m = re.search(r"Output written on .*?\((\d+) pages?", log_text)
    return int(m.group(1)) if m else None


def main(out_dir="out"):
    root = pathlib.Path(out_dir)
    logs = sorted(root.glob("*.log"))
    # drop pass-1 logs, they duplicate the final ones
    logs = [p for p in logs if not p.name.endswith(".pass1.log")]
    if not logs:
        print("no .log files found", file=sys.stderr)
        return 1

    failed = False
    print(f"{'SOURCE':52s} {'PAGES':>5s} {'OVERFULL':>9s} {'UNDERFULL':>10s}")
    print("-" * 82)
    for log in logs:
        text = log.read_text(errors="replace")
        pages = pages_from_log(text)
        over = len(re.findall(r"^Overfull \\hbox", text, re.M))
        under = len(re.findall(r"^Underfull \\hbox", text, re.M))
        name = log.stem
        flag = "" if pages == 1 else "  <-- NOT ONE PAGE"
        print(f"{name:52s} {str(pages):>5s} {over:>9d} {under:>10d}{flag}")
        if pages is None or pages != 1:
            failed = True

    print()
    if failed:
        print("RESULT: FAIL (a resume is not exactly one page)")
        return 1
    print("RESULT: PASS (all resumes are exactly one page)")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
