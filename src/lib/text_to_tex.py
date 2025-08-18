import os
import re

SPECIAL_LATEX_CHARS = [
    ('\\', r'\textbackslash{}'),  # single backslash first
    ('&', r'\&'),
    ('%', r'\%'),
    ('$', r'\$'),
    ('#', r'\#'),
    ('_', r'\_'),
    ('{', r'\{'),
    ('}', r'\}'),
    ('~', r'\textasciitilde{}'),
]

URL_PATTERN = re.compile(r'https?://\S+')

def escape_latex(text: str) -> str:
    if not text:
        return ''

    # Protect URLs first (so their underscores etc. are not escaped)
    protected_urls = []
    def url_placeholder(match):
        protected_urls.append(match.group(0))
        return f"@@URL{len(protected_urls)-1}@@"

    temp = URL_PATTERN.sub(url_placeholder, text)

    for old, new in SPECIAL_LATEX_CHARS:
        temp = temp.replace(old, new)

    # Restore URLs wrapped with \url{}
    for idx, url in enumerate(protected_urls):
        temp = temp.replace(f"@@URL{idx}@@", f"\\url{{{url}}}")
    return temp

def format_key_value(line: str) -> str:

    if line.startswith('- '):
        return None
    if ':' not in line:
        return None
    # Split only first colon
    key, value = line.split(':', 1)
    if not key.strip() or not value.strip():
        return None
    return f"\\textbf{{{escape_latex(key.strip())}:}} {escape_latex(value.strip())}"

def text_to_tex(text_file_path):
    r"""Converts a plain text file (with light markdown style) to LaTeX.

    Supported rules:
    - Markdown headings: #, ##, ### -> \section, \subsection, \subsubsection
    - Isolated headings without '#' (surrounded by blank lines) -> \section
    - Consecutive '- ' lines -> itemize list
    - 'Label: Value' -> Label in bold followed by forced line break
    - Basic **bold** and *italic*
    - URLs converted to \url{}
    """
    if not os.path.exists(text_file_path):
        raise FileNotFoundError(f"File not found: {text_file_path}")

    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            raw = f.read()

        raw_lines = [ln.rstrip() for ln in raw.splitlines()]
        latex = []
        in_list = False

        def close_list():
            nonlocal in_list
            if in_list:
                latex.append('\\end{itemize}')
                in_list = False

        def is_plain_paragraph_heading(idx):
            line = raw_lines[idx].strip()
            if not line or line.startswith(('#', '- ')) or ':' in line:
                return False
            prev_blank = (idx == 0) or (not raw_lines[idx-1].strip())
            next_blank = (idx == len(raw_lines)-1) or (not raw_lines[idx+1].strip())
            return prev_blank and next_blank and len(line) <= 120

        def emit_heading(text, level):
            close_list()
            mapping = {1: 'section', 2: 'subsection', 3: 'subsubsection'}
            cmd = mapping.get(level, 'paragraph')
            latex.append(f"\\{cmd}{{{escape_latex(text)}}}")

        i = 0
        while i < len(raw_lines):
            stripped = raw_lines[i].strip()
            if not stripped:
                close_list()
                i += 1
                continue

            # Markdown headings
            if stripped.startswith('#'):
                hashes = len(stripped) - len(stripped.lstrip('#'))
                title = stripped.lstrip('#').strip()
                if title:
                    emit_heading(title, hashes)
                    i += 1
                    continue

            # Plain isolated heading
            if is_plain_paragraph_heading(i):
                emit_heading(stripped, 1)
                i += 1
                continue

            # Bullet lines
            if stripped.startswith('- '):
                if not in_list:
                    latex.append('\\begin{itemize}')
                    in_list = True
                latex.append(f"\\item {escape_latex(stripped[2:].strip())}")
                i += 1
                continue

            # Key: Value
            kv = format_key_value(stripped)
            if kv:
                close_list()
                latex.append(kv + r"\\")
                i += 1
                continue

            # Inline formatting (**bold**, *italic*) preserving macros
            close_list()
            line_original = stripped
            placeholders = []

            def store(replacement):
                token = f"@@PH{len(placeholders)}@@"
                placeholders.append((token, replacement))
                return token

            # Bold
            def bold_sub(m):
                inner = escape_latex(m.group(1))
                return store(f"\\textbf{{{inner}}}")

            # Italic (single *) - avoid conflict with bold already replaced
            def italic_sub(m):
                inner = escape_latex(m.group(1))
                return store(f"\\textit{{{inner}}}")

            tmp = re.sub(r'\*\*(.+?)\*\*', bold_sub, line_original)
            tmp = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', italic_sub, tmp)

            # Escape rest (without touching placeholders)
            escaped = escape_latex(tmp)
            for token, repl in placeholders:
                escaped = escaped.replace(token, repl)
            # Añadir salto de línea LaTeX al final de cada línea normal
            latex.append(escaped + r"\\")
            i += 1

        close_list()
        return "\n".join(latex)
    except Exception as e:
        print(f"Error converting {text_file_path}: {e}")
        return None

