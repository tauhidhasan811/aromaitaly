from docx import Document
import fitz


def ReadDocx(file_path):
    print(' '* 60)
    print(file_path)
    print(' '* 60)
    doc = Document(file_path)

    text_data = ""
    for p in doc.paragraphs:
        text_data += " " + p.text
    return text_data

def ReadPdf(file_path: str):
    doc = fitz.open(file_path)
    
    extracted_text = ""
    for page_index, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            extracted_text += f"\n--- Page {page_index + 1} ---\n{text}"

    return extracted_text