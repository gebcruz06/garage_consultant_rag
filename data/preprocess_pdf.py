import fitz
import os
from PIL import Image
import io

def convert_pdf_to_markdown(input_pdf, output_md, image_dir):

    try:
        # Create output directories if they don't exist
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)

        doc = fitz.open(input_pdf)
        markdown_output = []

        # Track images to avoid saving duplicates
        image_references = {}

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            
            # Extract and process text
            text = page.get_text()
            markdown_output.append(text)
            
            # Extract and process images
            images = page.get_images(full=True)
            for img_index, img_info in enumerate(images):
                try:
                    xref = img_info[0]
                    
                    # Only process each unique image once
                    if xref not in image_references:
                        base_filename = os.path.splitext(os.path.basename(input_pdf))[0]
                        
                        # Generate a unique filename for the image
                        image_filename = f"{base_filename}_page_{page_num+1}_img_{img_index+1}.png"
                        image_path = os.path.join(image_dir, image_filename)
                        
                        # Extract the raw image
                        image_dict = doc.extract_image(xref)
                        img_bytes = image_dict["image"]
                        img_ext = image_dict["ext"]
                        
                        # Open with PIL to normalize to PNG
                        img_data = Image.open(io.BytesIO(img_bytes))
                        img_data = img_data.convert("RGB")  # normalize
                        img_data.save(image_path, format="PNG")
                        
                        image_references[xref] = image_filename

                    # Add Markdown reference to the image
                    image_filename = image_references[xref]
                    
                    # Use a relative path for markdown
                    relative_image_path = os.path.join('images', image_filename)
                    
                    markdown_output.append(f"\n![Image]({relative_image_path})\n")
                
                except Exception as e:
                    print(f"Failed to process image {img_index+1} on page {page_num+1}: {e}")
                    markdown_output.append(f"\n[Could not extract image {img_index+1} from page {page_num+1}]\n")
                    continue

        # Join all parts and save to the markdown file
        final_markdown = "\n".join(markdown_output)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(final_markdown)

        print(f"Conversion complete!\nMarkdown saved at: {output_md}")
        print(f"Images saved to: {image_dir}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Define the root directories
input_dir = "data/raw"
output_dir = "data/processed"
images_dir = os.path.join(output_dir, 'images')

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_pdf = os.path.join(input_dir, filename)
        
        # Define output file and image directory based on the PDF filename
        base_filename = os.path.splitext(filename)[0]
        output_md = os.path.join(output_dir, f"{base_filename}.md")

        # Run the conversion for the current PDF
        convert_pdf_to_markdown(input_pdf, output_md, images_dir)
