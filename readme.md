

# CV Creator

Generate a professional LaTeX/PDF résumé from structured YAML, Markdown, and plain text files. Organize your CV content in modular sections, then compile them into a single, polished PDF with one command.

---


## Prerequisites

- Python 3.8 or newer
- TeX Live with required LaTeX packages:

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

The output will be generated at: `output/cv.pdf`

---


## GitHub Actions Automation

You can automate PDF generation and delivery using GitHub Actions:

1. **Fork this repository** to your GitHub account.
2. **Prepare an API endpoint** that can receive a PDF file via HTTP POST (you'll need the API URL and optionally a bearer token).
3. **Set up repository secrets**:
	 - Go to your forked repo > Settings > Secrets and variables > Actions.
	 - Add the following as **Repository secrets**:
		 - `API_URL`: The endpoint to send the PDF.
		 - `API_TOKEN`: (optional) Bearer token for your API.
4. **Edit section files** in `cv_data/sections/` to update your CV.
5. **Commit and push** to `main`. The workflow runs automatically on changes or manual trigger.
6. The workflow will:
	- Install all dependencies (Python, TeX Live, etc.)
	- Build the PDF from your section files
	- Send the generated `cv.pdf` to your API endpoint

See `.github/workflows/build-and-send.yml` for details. No manual action is needed after setup—just edit your CV files and push!

---


## Personal Information Formatting

The `Personal Information` section is specially formatted for a clean, centered header at the top of your PDF. This is handled by the `format_personal_info_section` function in `src/lib/format_tex.py`.

**How it works:**
- The formatter looks for a section titled `Personal Information` (from your YAML file `01_personal_info.yaml`).
- It extracts:
	- `name`
	- `location`
	- `contacts` (with subfields: `email`, `phone`, `github`)
- These fields are rendered in a visually appealing, centered block at the top of the document.
- Only these fields are supported in the header. For more personal details (like languages or hobbies), add them as separate sections.

**Important:**
- Do not remove or rename the `Personal Information` section in your YAML. Otherwise, the special formatting will not be applied.
- For additional information, create new sections (e.g., `Languages`, `Hobbies`) after the personal info section.

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
- Special LaTeX characters are safely escaped (see `clean_latex_content` in `src/lib/yaml_to_tex.py`).

### Markdown (`.md`)
- Converted with Pandoc via `pypandoc` (see `src/lib/mkdocs_to_tex.py`).
- Headings, lists, emphasis, links, and more are supported.

### Text (`.txt`)
- Treated as Markdown and converted via Pandoc (see `src/lib/mkdocs_to_tex.py`).
- Headings: `#`, `##`, `###` → `\section`, `\subsection`, `\subsubsection`
- Isolated lines (surrounded by blanks) → `\section`
- `- ` prefix → bullet list
- `Label: Value` → bold label + forced line break
- Inline `**bold**` and `*italic*`
- URLs are automatically hyperlinked (see `url_replacer` in `src/lib/format_tex.py`).

### LaTeX (`.tex`)
- Copied verbatim into the final document (for custom formatting)

---



## How It Works

- `src/main.py`: Scans `cv_data/sections`, converts each file by extension, concatenates LaTeX, wraps with a preamble, and compiles to PDF.
- `lib/latex_template.py`: Provides the LaTeX preamble and document wrapper.
- `lib/mkdocs_to_tex.py`: Converts Markdown and text files to LaTeX using Pandoc.
- `lib/yaml_to_tex.py`: Recursively maps YAML to LaTeX sections, subsections, and lists, with LaTeX-safe escaping.
- `lib/tex_to_pdf.py`: Runs `pdflatex` to generate the PDF and cleans up auxiliary files.
- `lib/format_tex.py`: Post-processes the LaTeX for formatting, including URL hyperlinking and personal info layout.

---


## Tips

- Control section order by filename prefix (e.g., `01_`, `02_`, ...)
- You can add a custom `.tex` section for advanced formatting
- Keep line lengths reasonable in `.txt` for best heading detection

---

## Troubleshooting

### PDF is not generated or `output/cv.pdf` is missing
- Make sure you have TeX Live and all required LaTeX packages installed (see Prerequisites).
- Check for errors in the terminal output when running `python src/main.py`.
- If you see `pdflatex is not installed or not in the PATH`, install TeX Live as described above.

### "Error during LaTeX compilation" or build fails
- Review the error message for missing LaTeX packages or syntax errors in your section files.
- Ensure your YAML, Markdown, and text files are valid and do not contain unescaped special LaTeX characters.
- Try building with only a minimal set of sections to isolate the problematic file.

### Unicode or encoding errors
- Ensure all your section files are saved as UTF-8.
- Avoid using unsupported characters in your YAML, Markdown, or text files.

### Pandoc or pypandoc errors
- Make sure `pypandoc` and its dependencies are installed (`pip install -r requirements.txt`).
- If you see errors about missing `pandoc`, try installing it manually or ensure `pypandoc_binary` is installed.

### Custom formatting is not applied to Personal Information
- The YAML section must be named exactly `personal_information`.
- Only the fields `name`, `location`, and `contacts` (with subfields) are supported in the header.
- For additional info, add new sections after the personal info section.

### Still having issues?
- Run with only one or two section files to debug.
- Check the output in `output/cv.tex` for LaTeX errors.
- Open an issue or ask for help with your error message and a sample of your input files.



