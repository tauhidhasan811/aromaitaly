import os
from fastapi.exceptions import HTTPException
from .file_reader import ReadDocx, ReadPdf


def extract_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        #text, _ = extract_pdf_text_and_images(file_path)
        text= ReadPdf(file_path)

    elif ext == ".docx":
        text = ReadDocx(file_path=file_path)

    else:
        return HTTPException(status_code=403,detail=f"Unsupported file type: {ext}")
        # text = f"Unsupported file type: {ext}"
    return text
