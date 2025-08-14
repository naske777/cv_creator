import re

# Formats raw URLs throughout the document (except those already in \href or \url)
def url_replacer(tex):
    url_pattern = re.compile(r'https?://[\w\-\./\?\#\=\&\%\~\:]+', re.UNICODE)
    def replacer(match):
        url = match.group(0)
        start = match.start()
        before = tex[max(0, start-10):start]
        if before.endswith('\\href{') or before.endswith('\\url{'):
            return url
        display = url.replace('https://', '').replace('http://', '')
        return r'\href{' + url + '}{' + display + '}'
    return url_pattern.sub(replacer, tex)

def remove_section_numbering(tex):
    tex = re.sub(r'\\section{', r'\\section*{', tex)
    tex = re.sub(r'\\subsection{', r'\\subsection*{', tex)
    tex = re.sub(r'\\subsubsection{', r'\\subsubsection*{', tex)
    return tex

def format_personal_info_section(tex):

    personal_info_pattern = re.compile(r'\\section\*\{Personal Information\}(.+?)(?=\\section\*|\\end\{document\})', re.DOTALL)
    match = personal_info_pattern.search(tex)
    if not match:
        return tex
    block = match.group(1)
    
    # Extracts name and location
    name_match = re.search(r'\\textbf\{Name:} (.+?)\\\\', block)
    location_match = re.search(r'\\textbf\{Location:} (.+?)\\\\', block)
    name = name_match.group(1).strip() if name_match else ''
    location = location_match.group(1).strip() if location_match else ''

    after_location = block.split('\\textbf{Location:}', 1)[-1]
    contacts_block = after_location

    contact_values = re.findall(r'\\textbf\{[^}]+:} (.+?)\\\\', contacts_block)

    # Groups contacts in sets of 3
    contact_lines = []
    for i in range(0, len(contact_values), 3):
        contact_lines.append('  |  '.join(contact_values[i:i+3]))

    # Builds the custom LaTeX block
    custom = [r'\begin{center}']
    if name:
        custom.append(r'{\LARGE\textbf{' + name + r'}}\\')
    if location:
        custom.append(location + r'\\')
    for line in contact_lines:
        custom.append(line + r'\\')
    custom.append(r'\end{center}')

    # Replaces the original block
    return personal_info_pattern.sub(lambda m: ''.join(custom), tex)

def format_tex(tex):
    tex = url_replacer(tex)
    tex = remove_section_numbering(tex)
    tex = format_personal_info_section(tex)
    return tex