import fitz
import os
from PIL import Image
import io

def convert_pdf_to_markdown(input_pdf, output_md, image_dir, dpi=200):
    try:
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        doc = fitz.open(input_pdf)
        markdown_output = []
        base_filename = os.path.splitext(os.path.basename(input_pdf))[0]

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # Extract text
            text = page.get_text()
            if text.strip():  # Only add non-empty text
                markdown_output.append(text.strip())

            # Render full page as image
            try:
                page_img_filename = f"{base_filename}_page_{page_num+1}_full.png"
                page_img_path = os.path.join(image_dir, page_img_filename)
                
                page.get_pixmap(dpi=dpi, alpha=False).save(page_img_path)
                relative_path = os.path.join('images', page_img_filename)
                markdown_output.append(f"\n![Full Page]({relative_path})\n")

            except Exception as e:
                print(f"Failed to render page {page_num+1}: {e}")

            markdown_output.append("\n---\n")

        with open(output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))

        print(f"Conversion complete!\nMarkdown: {output_md}\nImages: {image_dir}")

    except Exception as e:
        print(f"Error: {e}")

# Main execution
input_dir = "data/raw"
output_dir = "data/processed"
images_dir = os.path.join(output_dir, 'images')

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_pdf = os.path.join(input_dir, filename)
        output_md = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.md")
        convert_pdf_to_markdown(input_pdf, output_md, images_dir)