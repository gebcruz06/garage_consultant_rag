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
        image_references = {}

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # --- Extract text ---
            text = page.get_text()
            markdown_output.append(text)

            # --- Extract embedded images ---
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                try:
                    xref = img_info[0]
                    if xref not in image_references:
                        base_filename = os.path.splitext(os.path.basename(input_pdf))[0]
                        image_filename = f"{base_filename}_page_{page_num+1}_img_{img_index+1}.png"
                        image_path = os.path.join(image_dir, image_filename)

                        image_dict = doc.extract_image(xref)
                        img_bytes = image_dict["image"]

                        img_data = Image.open(io.BytesIO(img_bytes))
                        img_data = img_data.convert("RGB")
                        img_data.save(image_path, format="PNG")

                        image_references[xref] = image_filename

                    image_filename = image_references[xref]
                    relative_image_path = os.path.join('images', image_filename)
                    markdown_output.append(f"\n![Image]({relative_image_path})\n")

                except Exception as e:
                    print(f"Failed to extract embedded image {img_index+1} on page {page_num+1}: {e}")
                    markdown_output.append(f"\n[Could not extract image {img_index+1} from page {page_num+1}]\n")

            # --- Render full page as fallback ---
            try:
                pix = page.get_pixmap(dpi=dpi, alpha=False)
                base_filename = os.path.splitext(os.path.basename(input_pdf))[0]
                page_img_filename = f"{base_filename}_page_{page_num+1}_full.png"
                page_img_path = os.path.join(image_dir, page_img_filename)

                pix.save(page_img_path)
                relative_image_path = os.path.join('images', page_img_filename)
                markdown_output.append(f"\n![Full Page]({relative_image_path})\n")

            except Exception as e:
                print(f"Failed to render page {page_num+1}: {e}")

            # Add a page break for clarity
            markdown_output.append("\n---\n")

        final_markdown = "\n".join(markdown_output)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        print(f"Conversion complete!\nMarkdown saved at: {output_md}")
        print(f"Images saved to: {image_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")


input_dir = "data/raw"
output_dir = "data/processed"
images_dir = os.path.join(output_dir, 'images')

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_pdf = os.path.join(input_dir, filename)
        base_filename = os.path.splitext(filename)[0]
        output_md = os.path.join(output_dir, f"{base_filename}.md")
        convert_pdf_to_markdown(input_pdf, output_md, images_dir, dpi=200)
