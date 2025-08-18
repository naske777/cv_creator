import pypandoc
import os

def markdown_to_tex(markdown_file):

    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"File not found: {markdown_file}")
    
    try:
        return pypandoc.convert_file(markdown_file, 'latex')

    except Exception as e:
        print(f"Error converting {markdown_file}: {e}")
        return None


