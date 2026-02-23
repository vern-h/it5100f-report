#!/usr/bin/env python3
"""
Convert the Assignment 3 report notebook to HTML for GitHub Pages.
Run from the directory containing the notebooks:
  python convert_report_to_html.py

Requires: pip install nbconvert
"""

import subprocess
import sys
from pathlib import Path

NOTEBOOK = Path(__file__).parent / "IT5100F_Assignment_3_ipynb.ipynb"
OUTPUT_HTML = Path(__file__).parent / "index.html"

def main():
    if not NOTEBOOK.exists():
        print(f"Notebook not found: {NOTEBOOK}")
        sys.exit(1)
    try:
        import nbconvert
    except ImportError:
        print("Installing nbconvert...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
    cmd = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "html",
        "--output", str(OUTPUT_HTML.name),
        "--output-dir", str(OUTPUT_HTML.parent),
        "--embed-images",
        str(NOTEBOOK),
    ]
    subprocess.check_call(cmd)
    print(f"Generated: {OUTPUT_HTML}")
    print("Next: Create a GitHub repo, push index.html to the gh-pages branch or /docs, and enable GitHub Pages.")

if __name__ == "__main__":
    main()
