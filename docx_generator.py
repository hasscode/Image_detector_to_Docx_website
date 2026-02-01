from docx import Document

def create_docx(text: str, filename: str):
    document = Document()
    document.add_heading("Converted Document", level=1)
    document.add_paragraph(text)
    document.save(filename)
