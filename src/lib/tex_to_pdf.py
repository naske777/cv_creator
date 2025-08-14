import subprocess
import tempfile
import os

def tex_to_pdf(tex_path):
    output_dir = os.path.abspath("output")
    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
        
    try:
        
        try:
            subprocess.run([
                "pdflatex",
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                "-jobname=cv",
                tex_path
            ], capture_output=True, text=True, check=True)

            if os.path.exists("output/cv.pdf"):
                print(f"✅ PDF generated: output/cv.pdf")
                return True
            else:
                print("❌ PDF file was not generated")
                return False
        finally:
                
            # Clean the output folder of non-PDF files
            for f in os.listdir(output_dir):
                if not (f.endswith(".pdf") or f.endswith(".tex")):
                    os.unlink(os.path.join(output_dir, f))

    except subprocess.CalledProcessError as e:
        print("❌ Error during LaTeX compilation:")
        print(e.stdout)
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("❌ pdflatex is not installed or not in the PATH")
        print("   Install TeX Live: https://www.tug.org/texlive/")
        return False