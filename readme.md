
# CV Creator

Generate a professional LaTeX/PDF résumé from structured YAML, Markdown, and plain text files. This project lets you organize your CV content in modular sections, then compiles them into a single, polished PDF.

---

## Prerequisites

- Python 3.8+
- Install TeX Live and required LaTeX packages:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
	texlive-latex-base \
	texlive-latex-recommended \
	texlive-latex-extra \
	texlive-fonts-recommended
```

Install Python dependencies from `requirements.txt`:

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

1. Place your section files in `cv_data/sections/`.
2. Name files with a prefix to control order (e.g., `01_`, `02_`, ...).
3. Build the PDF:

```bash
python src/main.py
```

Output: `output/cv.pdf`

---

## Using GitHub Actions

You can automate the generation and delivery of your PDF CV using GitHub Actions. Follow these steps:

1. **Fork this repository** to your own GitHub account.

2. **Prepare an API endpoint** that can receive a PDF file via HTTP POST. You will need the API URL and (optionally) a bearer token for authentication.

3. **Set up repository secrets**:
	- Go to your forked repository on GitHub.
	- Navigate to `Settings` > `Secrets and variables` > `Actions`.
	- Add the following secrets:
	  - `API_URL`: The endpoint where the PDF will be sent.
	  - `API_TOKEN`: (optional) Bearer token for your API.

4. **Edit the section files** in `cv_data/sections/` to update your CV content. You can add, remove, or modify any of the YAML, Markdown, or text files.

5. **Commit and push your changes** to the `main` branch of your fork. The GitHub Actions workflow will run automatically whenever you push changes to the section files or trigger the workflow manually.

6. **The workflow will:**
	- Install all dependencies (Python, TeX Live, etc.)
	- Build the PDF from your section files
	- Send the generated `cv.pdf` to your API endpoint

You can find the workflow file at `.github/workflows/build-and-send.yml`. No manual action is needed after setup—just edit your CV files and push!

---

## Personal Information Formatting

The `Personal Information` section in your CV is specially formatted for a clean, centered header at the top of your PDF. This formatting is handled by the `format_personal_info_section` function in `src/lib/format_tex.py`.

**How it works:**
- The formatter looks for a section titled `Personal Information` (from your YAML file `01_personal_info.yaml`).
- It extracts the following fields:
	- `name`
	- `location`
	- `contacts` (with subfields: `email`, `phone`, `github`)
- These fields are rendered in a visually appealing, centered block at the top of the document.
- Only these fields are supported in the header. If you want to include more personal details (like languages or hobbies), add them as separate sections in your CV.

**Important:**
- Do not remove or rename the `Personal Information` section in your YAML. If you do, the special formatting will not be applied and your header will not appear as intended.
- For any additional information, create new sections (e.g., `Languages`, `Hobbies`) after the personal info section.

**Example YAML (`cv_data/sections/01_personal_info.yaml`):**

```yaml
personal_information:
	name: Camila Torres
	location: Miami, FL
	contacts:
		email: camila.torres@email.com
		phone: "+1-786-555-0198"
		github: "https://github.com/camitorres"
```

## Features

- Mix and match input formats: `.yaml`, `.md`, `.txt`, and raw `.tex`
- Clean LaTeX output with safe escaping and hyperlink support
- One-command build: outputs `output/cv.pdf`
- Customizable section order via filename prefix (e.g., `01_`, `02_`)

---

## Project Structure

```
cv_creator/
├── cv_data/
│   └── sections/           # Place your section files here (ordered by filename)
│       ├── 01_personal_info.yaml
│       ├── 02_summary.md
│       ├── 03_experience.md
│       ├── 04_education.md
│       ├── 05_certifications.txt
│       ├── 06_awards.md
│       ├── 07_projects.md
│       └── 08_skills.yaml
├── output/                 # Generated files (cv.pdf, cv.tex)
├── src/
│   ├── main.py             # Orchestrates conversion and PDF build
│   └── lib/
│       ├── latex_template.py    # LaTeX preamble and document wrapper
│       ├── mkdocs_to_tex.py     # Markdown → LaTeX via pypandoc
│       ├── text_to_tex.py       # Text with light markdown → LaTeX
│       ├── yaml_to_tex.py       # YAML → LaTeX sections/lists
│       ├── tex_to_pdf.py        # pdflatex runner → PDF
│       └── format_tex.py        # Post-processing and formatting
└── readme.md
```

---

## Supported Input Formats

### YAML (`.yaml`)
- Top-level keys become sections; nested keys become subsections.
- Simple key–value pairs render as bold labels with line breaks.
- Lists render as `itemize` lists; list items that are dicts join their fields inline.
- Special LaTeX characters are safely escaped.

### Markdown (`.md`)
- Converted with Pandoc via `pypandoc`.
- Headings, lists, emphasis, links, and more are supported.

### Text (`.txt`)
- Headings: `#`, `##`, `###` → `\section`, `\subsection`, `\subsubsection`
- Isolated lines (surrounded by blanks) → `\section`
- `- ` prefix → bullet list
- `Label: Value` → bold label + forced line break
- Inline `**bold**` and `*italic*`
- URLs wrapped as `\url{...}`

### LaTeX (`.tex`)
- Copied verbatim into the final document (for custom formatting)

---

## How It Works

- `src/main.py`: Scans `cv_data/sections`, converts each file by extension, concatenates LaTeX, wraps with a preamble, and compiles to PDF.
- `lib/latex_template.py`: Provides the LaTeX preamble and document wrapper.
- `lib/mkdocs_to_tex.py`: Converts Markdown to LaTeX using Pandoc.
- `lib/text_to_tex.py`: Escapes LaTeX, handles lists, headings, inline styles, and URLs.
- `lib/yaml_to_tex.py`: Recursively maps YAML to sections, subsections, and lists.
- `lib/tex_to_pdf.py`: Runs `pdflatex` to generate the PDF and cleans up auxiliary files.
- `lib/format_tex.py`: Post-processes the LaTeX for formatting and personal info layout.

---

## Tips

- Control section order by filename prefix (e.g., `01_`, `02_`, ...)
- You can add a custom `.tex` section for advanced formatting
- Keep line lengths reasonable in `.txt` for best heading detection



