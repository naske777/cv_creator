def create_latex_document(content):
    """
    Wraps the content in a complete LaTeX document with preamble
    """
    preamble = r"""
\documentclass[11pt,a4paper]{article}

% Required packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}

% Page configuration
\geometry{margin=1in}
\pagestyle{empty}

% Hyperref configuration
\hypersetup{
    colorlinks=true,
    linkcolor=black,
    urlcolor=blue,
    citecolor=black
}

% Command for tightlist (used by pandoc)
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

\begin{document}

""".strip()

    ending = r"""

\end{document}
""".strip()

    return preamble + "\n\n" + content + "\n\n" + ending