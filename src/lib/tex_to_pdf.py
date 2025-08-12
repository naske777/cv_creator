import subprocess
import tempfile
import os

def tex_to_pdf(tex_content):
    output_dir = os.path.abspath("output")
    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
        
    try:
        # Create a temporary file to pass to pdflatex
        with tempfile.NamedTemporaryFile(suffix='.tex', prefix='cv', delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(tex_content.encode('utf-8'))
        
        try:
            subprocess.run([
                "pdflatex",
                "-interaction=nonstopmode",
                f"-output-directory={output_dir}",
                "-jobname=cv",
                tmp_path
            ], capture_output=True, text=True, check=True)

            if os.path.exists("output/cv.pdf"):
                print(f"✅ PDF generated: output/cv.pdf")
                return True
            else:
                print("❌ PDF file was not generated")
                return False
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
            # Clean the output folder of non-PDF files
            for f in os.listdir(output_dir):
                if not f.endswith(".pdf"):
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