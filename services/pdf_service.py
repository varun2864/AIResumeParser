#extracts text from pdf

import pdfplumber
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:    
    
    text_parts = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text())

    return "\n".join(text_parts)