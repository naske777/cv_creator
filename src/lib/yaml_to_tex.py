import yaml

def clean_latex_content(value):
    if not isinstance(value, str):
        return value
    
    value = value.strip()
    
    replacements = [
        ('\\', r'\textbackslash{}'),  
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('\n', ' '),
        ('  ', ' ')
    ]
    
    for old, new in replacements:
        value = value.replace(old, new)
    
    return value

def yaml_to_tex(yaml_file_or_data, parent_key="", depth=0):
    """
    Converts YAML file or YAML data to STANDARD LaTeX
    
    Args:
        yaml_file_or_data: Path to .yaml file or already loaded data
        parent_key: Parent key for recursion
        depth: Recursion depth
    
    Returns:
        str: Generated standard LaTeX content
    """
    # If it's a string, assume it's a file path
    if isinstance(yaml_file_or_data, str) and depth == 0:
        with open(yaml_file_or_data, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    else:
        data = yaml_file_or_data
    
    tex = []
    
    if isinstance(data, dict):
        # If we are at the root level, the first key is the main title
        if depth == 0:
            for key, value in data.items():
                section_title = key.replace('_', ' ').title()
                # The content can be dict, list, or simple value
                tex.append(yaml_to_tex(value, section_title, depth+1))
        else:
            # Determine section type by depth
            if depth == 1:
                section_cmd = "\\section"
            elif depth == 2:
                section_cmd = "\\subsection"
            else:
                section_cmd = "\\subsubsection"
            tex.append(f"{section_cmd}{{{parent_key}}}")

            # If the dict has only simple values, show each field on a separate line
            simple_values = all(isinstance(v, (str, int, float, bool)) for v in data.values())
            if simple_values:
                for key, value in data.items():
                    tex.append(f"\\textbf{{{key.replace('_', ' ').title()}:}} {clean_latex_content(value)}\\\\")
            else:
                # If there are dicts or lists, process recursively
                for key, value in data.items():
                    if isinstance(value, dict):
                        tex.append(yaml_to_tex(value, key.replace('_', ' ').title(), depth+1))
                    elif isinstance(value, list):
                        tex.append(yaml_to_tex(value, key.replace('_', ' ').title(), depth+1))
                    else:
                        tex.append(f"\\textbf{{{key.replace('_', ' ').title()}:}} {clean_latex_content(value)}\\\\")
    
    elif isinstance(data, list):
        # Show lists as itemize, using section command according to depth
        if parent_key:
            if depth == 1:
                section_cmd = "\\section"
            elif depth == 2:
                section_cmd = "\\subsection"
            else:
                section_cmd = "\\subsubsection"
            tex.append(f"{section_cmd}{{{parent_key}}}")
        tex.append("\\begin{itemize}")
        for item in data:
            if isinstance(item, dict):
                # Show all fields of the dict
                item_parts = []
                for k, v in item.items():
                    item_parts.append(f"{k.replace('_', ' ').title()}: {clean_latex_content(v)}")
                tex.append(f"\\item {'; '.join(item_parts)}")
            else:
                tex.append(f"\\item {clean_latex_content(item)}")
        tex.append("\\end{itemize}")
    
    else:
        # Simple value: just the cleaned content
        tex.append(clean_latex_content(data))
    
    return "\n".join(tex)
