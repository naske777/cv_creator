import os
import glob

# Import conversion functions
from lib.tex_to_pdf import tex_to_pdf
from lib.yaml_to_tex import yaml_to_tex
from lib.mkdocs_to_tex import markdown_to_tex  
from lib.text_to_tex import text_to_tex
from lib.latex_template import create_latex_document
from lib.format_tex import format_tex

def process_folder_content_to_tex(folder="cv_data/sections"):
    """
    Reads all files in the folder and generates a complete LaTeX file.
    Only supports md, yaml, and txt formats.
    Args:
        folder: Directory with files to convert
    """
    
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Directory not found: {folder}")
    
    # Get all files and sort them
    all_files = glob.glob(os.path.join(folder, "*"))
    all_files.sort()  
    
    latex_content = []
    
    print(f"Processing files in {folder}:")
    print("-" * 50)
    
    for file_path in all_files:
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1].lower()
        
        print(f"Processing: {filename}")
        
        try:
            if file_ext == '.yaml':
                content = yaml_to_tex(file_path)
                
            elif file_ext == '.md':
                content = markdown_to_tex(file_path)
                
            elif file_ext == '.txt':
                content = text_to_tex(file_path)
                
            elif file_ext == '.tex':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
            else:
                print(f"  ⚠️  Unsupported file type: {file_ext}")
                continue
            
            if content:
                latex_content.append(content.strip())
                latex_content.append("")  # Blank line
                print(f"  ✅ Successfully converted")
            else:
                print(f"  ❌ Error in conversion")
                
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    final_latex = "\n".join(latex_content)

    print("-" * 50)
    print(f"📊 Total sections processed: {len([f for f in all_files if os.path.splitext(f)[1] in ['.yaml', '.md', '.txt', '.tex']])}")
    
    complete_document = create_latex_document(final_latex)

    complete_document = format_tex(complete_document)

    os.makedirs("output", exist_ok=True)
    
    # guarda el latex en local
    tex_path = os.path.join("output", "cv.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(complete_document)
        
    tex_to_pdf(tex_path)
    return complete_document

if __name__ == "__main__":
    result = process_folder_content_to_tex()
