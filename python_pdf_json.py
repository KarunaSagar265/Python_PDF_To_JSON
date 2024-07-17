import fitz
#fitz is PyMuPDF
import json

def pdf_to_json(pdf_path, json_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    pdf_data = {"pages": []}

    # Iterate through each page
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        
        pdf_data["pages"].append({
            "page_number": page_num + 1,
            "text": text
        })

    # Write the data to a JSON file
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(pdf_data, json_file, ensure_ascii=False, indent=4)


pdf_path = "/content/CV_Karuna Sagar.pdf"
json_path = "/content/output.json"
pdf_to_json(pdf_path, json_path)
