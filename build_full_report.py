#!/usr/bin/env python3
"""
Build a single combined report from Assignments 1, 2, and 3, then export to index.html.
Run from the directory containing the notebooks:
  python build_full_report.py

Output: Full_Report.ipynb and index.html (all-in-one report for GitHub Pages).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
A1 = DIR / "IT5100F_Assignment_1.ipynb"
A2 = DIR / "IT5100F_A2_5.ipynb"
A3 = DIR / "IT5100F_Assignment_3_ipynb.ipynb"
FULL_NB = DIR / "Full_Report.ipynb"
OUTPUT_HTML = DIR / "index.html"


def sanitize_id(cell):
    """Ensure cell id matches ^[a-zA-Z0-9-_]+$ (no dots)."""
    if "id" in cell.get("metadata", {}):
        mid = cell["metadata"]["id"]
        if mid and not re.match(r"^[a-zA-Z0-9_-]+$", mid):
            cell["metadata"]["id"] = re.sub(r"[^a-zA-Z0-9_-]", "-", mid)
    if "id" in cell:
        cid = cell["id"]
        if cid and not re.match(r"^[a-zA-Z0-9_-]+$", cid):
            cell["id"] = re.sub(r"[^a-zA-Z0-9_-]", "-", cid)
    return cell


def ensure_stream_name(output):
    """Ensure stream output has 'name' (stdout/stderr)."""
    if output.get("output_type") == "stream" and "name" not in output:
        output["name"] = "stdout"
    return output


def ensure_output_metadata(output):
    """Ensure execute_result has metadata and execution_count; stream has no metadata."""
    ot = output.get("output_type")
    if ot == "execute_result":
        if "metadata" not in output:
            output["metadata"] = {}
        if "execution_count" not in output:
            output["execution_count"] = None
    elif ot == "stream" and "metadata" in output:
        del output["metadata"]  # stream must not have metadata per schema
    elif ot in ("display_data", "error") and "metadata" not in output:
        output["metadata"] = {}
    return output


def load_and_sanitize(path, id_prefix=""):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    for i, cell in enumerate(nb.get("cells", [])):
        sanitize_id(cell)
        if id_prefix:
            uid = cell.get("metadata", {}).get("id") or cell.get("id") or f"cell-{i}"
            uid = re.sub(r"[^a-zA-Z0-9_-]", "-", str(uid))
            new_id = f"{id_prefix}-{uid}" if uid else f"{id_prefix}-{i}"
            cell["metadata"]["id"] = new_id
            cell["id"] = new_id
        for out in cell.get("outputs", []):
            ensure_stream_name(out)
            ensure_output_metadata(out)
    return nb


def main():
    for path in (A1, A2, A3):
        if not path.exists():
            print(f"Missing: {path}")
            sys.exit(1)

    nb1 = load_and_sanitize(A1, "a1")
    nb2 = load_and_sanitize(A2, "a2")
    nb3 = load_and_sanitize(A3, "a3")

    # Combined notebook: use A3 metadata (kernelspec etc.), nbformat from A1
    combined = {
        "cells": [],
        "metadata": nb3.get("metadata", {}),
        "nbformat": nb1.get("nbformat", 4),
        "nbformat_minor": nb1.get("nbformat_minor", 5),
    }

    # Title cell
    combined["cells"].append({
        "cell_type": "markdown",
        "metadata": {"id": "full-report-title"},
        "id": "full-report-title",
        "source": [
            "# IT5100F Final Report: E-Commerce Orders\n"
        ]
    })

    # Assignment 1
    combined["cells"].append({
        "cell_type": "markdown",
        "metadata": {"id": "part-a1-header"},
        "id": "part-a1-header",
        "source": ["## Part 1: Assignment 1 — Data Preprocessing and EDA\n", "\n", "---"]
    })
    combined["cells"].extend(nb1["cells"])

    # Assignment 2
    combined["cells"].append({
        "cell_type": "markdown",
        "metadata": {"id": "part-a2-header"},
        "id": "part-a2-header",
        "source": ["\n", "## Part 2: Assignment 2 — Supervised Learning\n", "\n", "---"]
    })
    combined["cells"].extend(nb2["cells"])

    # Assignment 3
    combined["cells"].append({
        "cell_type": "markdown",
        "metadata": {"id": "part-a3-header"},
        "id": "part-a3-header",
        "source": ["\n", "## Part 3: Assignment 3 — Unsupervised Learning & Association Mining\n", "\n", "---"]
    })
    combined["cells"].extend(nb3["cells"])

    with open(FULL_NB, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Written: {FULL_NB}")

    # Export to HTML
    try:
        import nbconvert
    except ImportError:
        print("Installing nbconvert...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
    subprocess.check_call([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "html",
        "--output", OUTPUT_HTML.name,
        "--output-dir", str(OUTPUT_HTML.parent),
        "--embed-images",
        str(FULL_NB),
    ])
    print(f"Generated: {OUTPUT_HTML}")
    print("Push index.html to your repo and enable GitHub Pages (see README).")


if __name__ == "__main__":
    main()
