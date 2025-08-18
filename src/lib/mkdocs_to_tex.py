import pypandoc
import os

def markdown_to_tex(markdown_file):

    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"File not found: {markdown_file}")

    try:
        ext = os.path.splitext(markdown_file)[1].lower()
        if ext in ('.md', '.txt'):
            with open(markdown_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Añadir dos espacios al final de cada línea no vacía para forzar salto de línea en Markdown
            content = ''.join([(line.rstrip() + '  \n') if line.strip() else '\n' for line in lines])
            return pypandoc.convert_text(content, 'latex', format='md')
        else:
            raise ValueError(f"Unsupported file extension for markdown_to_tex: {ext}")
    except Exception as e:
        print(f"Error converting {markdown_file}: {e}")
        return None


