# IT5100F Final Report — E-Commerce Orders

Combined report for **Assignment 1** (data cleaning & EDA), **Assignment 2** (supervised learning), and **Assignment 3** (unsupervised learning & association mining).

## Build one `index.html` (all assignments)

From this directory:

```bash
python build_full_report.py
```

This merges the three notebooks into `Full_Report.ipynb` and exports **index.html** (single page, images embedded). Use this file for GitHub Pages.

## Publish on GitHub Pages (github.io)

Repo: **https://github.com/vern-h/it5100f-report**

### 1. Build the report

```bash
python build_full_report.py
```

### 2. Push to your repo

If you already did the first commit and remote:

```bash
git add index.html
git add README.md
git commit -m "Add full report (A1+A2+A3) and README"
git push -u origin main
```

### 3. Enable GitHub Pages

1. On GitHub: **Settings → Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main` — **Folder**: `/ (root)` (or choose **docs** if you put `index.html` in a `docs` folder)
4. Save. After a minute or two the site will be at:

**https://vern-h.github.io/it5100f-report/**

Put this URL in your Assignment 3 notebook under “Your published URL” and in your Canvas submission.

## Optional: push notebooks and build script

To keep the repo self-contained:

```bash
git add IT5100F_Assignment_1.ipynb IT5100F_A2_5.ipynb IT5100F_Assignment_3_ipynb.ipynb build_full_report.py
git commit -m "Add source notebooks and build script"
git push
```

You can add `Full_Report.ipynb` and `PUBLISH_GITHUB_PAGES.md` too if you like.
