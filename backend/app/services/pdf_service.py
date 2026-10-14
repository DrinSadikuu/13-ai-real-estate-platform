from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


class InvalidPDFError(Exception):
    pass


class EmptyPDFError(Exception):
    pass


class PDFService:
    def extract_text(self, file_content: bytes) -> str:
        try:
            pdf = PdfReader(BytesIO(file_content))

            text = ""

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        except (PdfReadError, ValueError, OSError) as exc:
            raise InvalidPDFError(
                "The uploaded PDF is corrupted or invalid"
            ) from exc

        text = text.strip()

        if not text:
            raise EmptyPDFError(
                "The uploaded PDF contains no extractable text"
            )

        return text