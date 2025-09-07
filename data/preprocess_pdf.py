import fitz
import os
import io
from PIL import Image

def convert_pdf_to_markdown(input_pdf, output_md, image_dir):

    try:
        # Create output directories if they don't exist
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        doc = fitz.open(input_pdf)
        markdown_output = []

        # Track images to avoid saving duplicates
        image_count = 0
        image_references = {}

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            
            # Extract and process text
            text = page.get_text()
            markdown_output.append(text)
            
            # Extract and process images
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                xref = img_info[0]
                if xref not in image_references:
                    image_count += 1
                    base_filename = os.path.splitext(os.path.basename(input_pdf))[0]
                    
                    # Generate a unique filename for the image
                    image_filename = f"{base_filename}_page_{page_num+1}_img_{img_index+1}.png"
                    image_path = os.path.join(image_dir, image_filename)
                    
                    # Extract and save the image
                    pix = fitz.Pixmap(doc, xref)
                    if pix.alpha:
                        # Convert to RGBA for saving with alpha channel
                        img_data = Image.open(io.BytesIO(pix.tobytes()))
                        img_data.save(image_path)
                    else:
                        pix.save(image_path)
                    
                    image_references[xref] = image_filename

                # Add Markdown reference to the image
                image_filename = image_references[xref]
                markdown_output.append(f"\n![Image {image_count}]({os.path.join(os.path.basename(image_dir), image_filename)})\n")

        # Join all parts and save to the markdown file
        final_markdown = "\n".join(markdown_output)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        print(f"Conversion complete!\nMarkdown saved at: {output_md}")
        print(f"Images saved to: {image_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define file paths
input_pdf = "data/raw/AVK310_P22(9900B-40257-010).pdf"
output_md = "data/processed/AVK310_P22(9900B-40257-010).md"

# Define the directory where images will be saved
image_dir = os.path.join(os.path.dirname(output_md), 'images')

# Run the conversion
convert_pdf_to_markdown(input_pdf, output_md, image_dir)