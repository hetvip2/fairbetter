import PyPDF2

def extract_text_from_pdf(pdf_stream):
    """
    Extracts text from a PDF file stream.
    """
    reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
