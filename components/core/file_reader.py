from docx import Document
import fitz


def ReadDocx(path):
    doc = Document(path)

    text_data = ""
    for p in doc.paragraphs:
        text_data += " " + p.text
    return text_data

def ReadPdf(pdf_path: str):
    doc = fitz.open(pdf_path)

    extracted_text = ""
    for page_index, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            extracted_text += f"\n--- Page {page_index + 1} ---\n{text}"

    return extracted_text