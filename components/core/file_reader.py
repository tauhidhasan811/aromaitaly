from docx import Document

def ReadDocx(path):
    doc = Document(path)

    text_data = ""
    for p in doc.paragraphs:
        text_data = text_data+ p.text
    return text_data
