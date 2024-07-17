import fitz
import json
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
from io import BytesIO
import base64

class ImageModel(BaseModel):
    page_number: int
    image_index: int
    image_base64: str

class PageModel(BaseModel):
    page_number: int
    text: str
    images: Optional[List[ImageModel]]
    #Image list is optional so it creates an empty list

class PDFModel(BaseModel):
    file_name: str
    pages: List[PageModel]
    #PDF base model, creates PDF model with empty page list

def extract_text_and_images(pdf_path: str) -> PDFModel:
    doc = fitz.open(pdf_path)
    pdf_data = PDFModel(file_name=pdf_path, pages=[])
    #pdf data is extraxted


    for page_number in range(len(doc)):
        page = doc[page_number]
        text = page.get_text("text")
        images = []
        #iterates over the page numbers and gets text

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            #images are converted to base 64 format and bytes are stored

            # Convert image to base64
            img_base64 = base64.b64encode(image_bytes).decode('utf-8') # image encoded
            images.append(ImageModel(page_number=page_number, image_index=img_index, image_base64=img_base64)) #image models are appended in the image model

        page_data = PageModel(page_number=page_number, text=text, images=images)#in page model the page number and 
        pdf_data.pages.append(page_data)

    return pdf_data

# Specify the PDF file path
pdf_file_path = '/content/Biology2e-WEB_Excerpt.pdf'

# Extract data and convert to JSON
pdf_data = extract_text_and_images(pdf_file_path)

# Convert to JSON using the json module
pdf_dict = pdf_data.dict()
pdf_json = json.dumps(pdf_dict, indent=4)

# Adding line spaces between different sections in the JSON string
pdf_json_with_spaces = pdf_json.replace('},', '},\n')

# Save JSON to a file
with open('output.json', 'w') as f:
    f.write(pdf_json_with_spaces)

print("PDF data has been saves as output.json.")
