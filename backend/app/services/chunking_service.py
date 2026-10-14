
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def split_text(self, text: str) -> list[str]:
        return self.splitter.split_text(text)
