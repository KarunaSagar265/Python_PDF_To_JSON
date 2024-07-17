import fitz  # PyMuPDF
import json
from pydantic import BaseModel
from typing import List, Optional
import os

class ImageModel(BaseModel):
    page_number: int
    image_index: int
    image_path: str

class PageModel(BaseModel):
    page_number: int
    text: str
    images: Optional[List[ImageModel]]

class PDFModel(BaseModel):
    file_name: str
    pages: List[PageModel]

def extract_text_and_images(pdf_path: str, image_dir: str) -> PDFModel:
    # Create the image directory if it does not exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    doc = fitz.open(pdf_path)
    pdf_data = PDFModel(file_name=pdf_path, pages=[])

    for page_number in range(len(doc)):
        page = doc[page_number]
        text = page.get_text("text")
        images = []

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # Get the image extension (e.g., png, jpeg)

            # Define the image file path
            image_path = os.path.join(image_dir, f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}")

            # Save the image to the file
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)

            images.append(ImageModel(page_number=page_number, image_index=img_index, image_path=image_path))

        page_data = PageModel(page_number=page_number, text=text, images=images)
        pdf_data.pages.append(page_data)

    return pdf_data

# Specify the PDF file path and image directory
pdf_file_path = '/content/Biology2e-WEB_Excerpt.pdf'
image_dir = 'extracted_images'

# Extract data and convert to JSON
pdf_data = extract_text_and_images(pdf_file_path, image_dir)

# Convert to JSON using the json module
pdf_dict = pdf_data.dict()
pdf_json = json.dumps(pdf_dict, indent=4)

# Adding line spaces between different sections in the JSON string
pdf_json_with_spaces = pdf_json.replace('},', '},\n')

# Save JSON to a file
with open('output.json', 'w') as f:
    f.write(pdf_json_with_spaces)

print("PDF data has been successfully converted to JSON with image paths and saved as 'output.json'.")
