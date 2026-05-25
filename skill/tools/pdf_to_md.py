#!/usr/bin/env python3
"""Convert PDFs in source/raw/ to markdown in stages/00_collect/output/.

Usage:
    python scripts/pdf_to_md.py                        # convert all PDFs in source/raw/
    python scripts/pdf_to_md.py path/to/file.pdf       # convert a single file
    python scripts/pdf_to_md.py file.pdf output.md     # convert with explicit output path

Requires: pymupdf4llm  (pip install pymupdf4llm)

Place this script at scripts/pdf_to_md.py inside the workspace root.
"""

import sys
import os
from pathlib import Path
import pymupdf4llm

WORKSPACE = Path(__file__).parent.parent
RAW_DIR = WORKSPACE / "source" / "raw"
OUT_DIR = WORKSPACE / "stages" / "00_collect" / "output"


def convert(pdf_path: Path, out_path: Path):
    print(f"  {pdf_path.name} -> {out_path.name}")
    md = pymupdf4llm.to_markdown(str(pdf_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        pdfs = sorted(RAW_DIR.glob("*.pdf"))
        if not pdfs:
            print(f"No PDFs found in {RAW_DIR}")
            sys.exit(1)
        print(f"Converting {len(pdfs)} PDF(s) to {OUT_DIR}/")
        for pdf in pdfs:
            convert(pdf, OUT_DIR / (pdf.stem + ".md"))

    elif len(args) == 1:
        pdf_path = Path(args[0])
        convert(pdf_path, OUT_DIR / (pdf_path.stem + ".md"))

    elif len(args) == 2:
        convert(Path(args[0]), Path(args[1]))

    else:
        print(__doc__)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
