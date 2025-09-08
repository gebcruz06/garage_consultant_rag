import os
from markitdown import MarkItDown

def convert_pdf_to_markdown(input_pdf, output_md):
    try:
        os.makedirs(os.path.dirname(output_md), exist_ok=True)

        md = MarkItDown()
        result = md.convert(input_pdf)

        with open(output_md, "w", encoding="utf-8") as f:
            f.write(result.text_content)

        print(f"Conversion complete!\nMarkdown: {output_md}")

    except Exception as e:
        print(f"Error: {e}")


# Main execution
input_dir = "data/raw"
output_dir = "data/processed"

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_pdf = os.path.join(input_dir, filename)
        output_md = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")
        convert_pdf_to_markdown(input_pdf, output_md)
