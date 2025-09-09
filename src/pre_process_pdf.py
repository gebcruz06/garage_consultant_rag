import os
from pymupdf4llm import to_markdown

def convert_pdf_to_markdown(input_pdf, output_md):

    try:
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        
        # Use pymupdf4llm's to_markdown function directly
        md_content = to_markdown(input_pdf)
        
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"Conversion complete!\nMarkdown: {output_md}")

    except Exception as e:
        print(f"Error: {e}")

# Main execution
input_dir = "data/raw"
output_dir = "data/processed"

if not os.path.exists(input_dir):
    print(f"Input directory '{input_dir}' not found.")
else:
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_dir, filename)
            output_md = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")
            convert_pdf_to_markdown(input_pdf, output_md)