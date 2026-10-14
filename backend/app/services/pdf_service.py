
from io import BytesIO

from pypdf import PdfReader


class PDFService:
    def extract_text(self, file_content: bytes) -> str:
        pdf = PdfReader(BytesIO(file_content))

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()
