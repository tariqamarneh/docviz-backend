from io import BytesIO

from docx import Document
from pypdf import PdfReader

from app.services.uploadfile import get_file, get_file_binary


def extract_text_from_pdf(binary: BytesIO) -> str:
    pdf = PdfReader(binary)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


def extract_text_from_docx(binary: BytesIO) -> str:
    document = Document(binary)
    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    return text


def extract_text_from_txt(binary: BytesIO) -> str:
    return binary.read().decode("utf-8")


extract_text = {
    "application/pdf": extract_text_from_pdf,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extract_text_from_docx,
    "text/plain": extract_text_from_txt,
}


async def extract_content(file_id: str):
    file = await get_file(file_id)
    file_type = file.metadata["content_type"]
    file_name = file.filename
    binary = await get_file_binary(file_id)
    text = extract_text[file_type](BytesIO(binary))
    return text, file_name
