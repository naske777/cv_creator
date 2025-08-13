## CV Creator — Build a polished LaTeX/PDF résumé from YAML, Markdown, and Text

Turn structured content in `cv_data/sections` into a single LaTeX document and compile it to a print‑ready PDF. Files are processed in lexicographic order, so prefix them (e.g., `01_`, `02_`) to control section ordering.

### Highlights
- Mix-and-match inputs: `.yaml`, `.md`, `.txt`, and even raw `.tex`
- Clean LaTeX output with hyperlink support and safe escaping
- Simple one-command build that writes `output/cv.pdf`

---

## Project layout
```
cv_creator/
├─ cv_data/
│  └─ sections/              # Drop your section files here (ordered by filename)
│     ├─ 01_personal_info.yaml
│     ├─ 02_summary.md
│     ├─ 03_experience.md
│     ├─ 04_education.md
│     ├─ 05_certifications.txt
│     ├─ 06_awards.md
│     ├─ 07_projects.md
│     └─ 08_skills.yaml
├─ output/                    # Built artifacts (cv.pdf)
├─ src/
│  ├─ main.py                 # Orchestrates conversion and PDF build
│  └─ lib/
│     ├─ latex_template.py    # Preamble and document wrapper
│     ├─ mkdocs_to_tex.py     # Markdown → LaTeX via pypandoc
│     ├─ text_to_tex.py       # Plain text with light markdown → LaTeX
│     ├─ yaml_to_tex.py       # YAML → LaTeX sections/lists
│     └─ tex_to_pdf.py        # pdflatex runner → PDF
└─ readme.md
```

---

## Prerequisites
- Python 3.8+
- Python packages: `PyYAML`, `pypandoc` (install below)
- TeX toolchain providing `pdflatex` (e.g., TeX Live or MiKTeX)
- Pandoc (recommended). Note: `pypandoc` can download a local Pandoc on first use, but a system Pandoc works best.

---

## Setup
```bash
# (Optional) use a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## Usage
1) Put your section files in `cv_data/sections/`.
2) Ensure filenames are ordered as you want them to appear.
3) Build the PDF:

```bash
python src/main.py
```

Output: `output/cv.pdf`

---

## Supported input formats

### YAML (`.yaml`)
- Top-level keys become sections; nested keys become subsections.
- Simple key–value maps render as bold labels with line breaks.
- Lists render as `itemize` lists; list items that are dicts join their fields inline.
- Special LaTeX characters are safely escaped.

### Markdown (`.md`)
- Converted with Pandoc via `pypandoc`.
- Headings, lists, emphasis, links, and more are supported by Pandoc’s Markdown.

### Text (`.txt`)
Lightweight rules in `text_to_tex.py`:
- `#`, `##`, `###` → `\section`, `\subsection`, `\subsubsection`
- Isolated plain lines (surrounded by blanks) → `\section`
- `- ` prefix → bullet list
- `Label: Value` → bold label + forced line break
- Inline `**bold**` and `*italic*`
- URLs preserved and wrapped as `\url{…}`

### LaTeX (`.tex`)
- Copied verbatim into the final document. Useful for custom formatting.

---

## How it works (file reference)
- `src/main.py`: Scans `cv_data/sections`, converts each file by extension, concatenates LaTeX, wraps with a preamble, and compiles to PDF.
- `lib/latex_template.py`: Minimal article preamble (geometry, hyperref, enumitem, titlesec) and `\tightlist` helper.
- `lib/mkdocs_to_tex.py`: Uses `pypandoc.convert_file(..., 'latex')` for Markdown → LaTeX.
- `lib/text_to_tex.py`: Escapes LaTeX, handles lists/headings/inline styles and `\url{}`.
- `lib/yaml_to_tex.py`: Recursively maps YAML → sections, subsections, and lists.
- `lib/tex_to_pdf.py`: Writes a temp `.tex` and runs `pdflatex` into `output/` (cleans non-PDF artifacts).

---

## Tips
- Control order by filename (e.g., `01_`, `02_`, ...).
- You can drop a fully custom `.tex` section for fine-grained control.
- Keep line lengths reasonable in `.txt` so isolated headings are detected cleanly.

---


## Troubleshooting
- `pdflatex is not installed or not in the PATH`: Install TeX Live or MiKTeX and ensure `pdflatex` is available.
- Pandoc missing: Install Pandoc or let `pypandoc` download a local copy.
- Compilation errors: Check special characters and unmatched LaTeX braces in your source sections.

---

## GitHub Actions: Build & Send PDF Automatically

This project includes a GitHub Actions workflow (`.github/workflows/build-and-send.yml`) that automates the generation and sending of the PDF every time you push to the `main` branch.

### What does the workflow do?

1. **Installs dependencies**: Python, required packages, and TeX Live (for `pdflatex`).
2. **Builds the PDF**: Runs `python src/main.py` and checks that `output/cv.pdf` was generated successfully.
3. **Sends the PDF to an API**: Uses `curl` to POST the PDF to a URL defined by the `API_URL` environment variable (and optionally a `API_TOKEN`).

### Required variables

- `API_URL`: The API endpoint to which the PDF will be sent (must be set as a GitHub secret).
- `API_TOKEN`: (optional) Bearer token for authentication.

---

