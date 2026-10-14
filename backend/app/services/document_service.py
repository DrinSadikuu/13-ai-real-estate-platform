import chunk
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.document_repository import DocumentRepository
from app.services.pdf_service import PDFService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.s3_service import S3Service


class DocumentService:
    def __init__(self, session: AsyncSession):
        self.repository = DocumentRepository(session)

        self.pdf_service = PDFService()
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.s3_service = S3Service()

    async def process_document(
        self,
        filename: str,
        file_content: bytes,
    ) -> dict:
        # Extract text
        extracted_text = self.pdf_service.extract_text(file_content)

        # Split into chunks
        chunks = self.chunking_service.split_text(extracted_text)

        # Generate embeddings
        embeddings = []

        for chunk in chunks:
            embedding = await self.embedding_service.generate_embedding(chunk)
            embeddings.append(embedding)

        # Upload PDF to AWS S3
        file_key = f"ai-real-estate/property-documents/{uuid4()}.pdf"

        self.s3_service.upload_file(file_content, file_key)

        # Save document in PostgreSQL
        document = await self.repository.create_document(
            filename=filename,
            s3_key=file_key,
        )

        # Save chunks and embeddings
        await self.repository.create_chunks(
            document_id=document.id,
            chunks=chunks,
            embeddings=embeddings,
        )

        # Save both operations in one transaction
        await self.repository.commit()

        return {
            "document_id": str(document.id),
            "filename": filename,
            "s3_key": file_key,
            "total_chunks": len(chunks),
            "total_embeddings": len(embeddings),
            "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
            "message": "Document uploaded, chunked, and saved successfully",
        }

    async def search_documents(
            self,
            query: str,
            limit: int = 5,
            document_id: UUID | None = None,
    ) -> list[dict]:
        # Generate embedding for the user's question
        query_embedding = await self.embedding_service.generate_embedding(
            query
        )

        # Search document chunks, optionally filtering by document ID
        chunks = await self.repository.search_similar_chunks(
            query_embedding=query_embedding,
            limit=limit,
            document_id=document_id,
        )

        # Return chunks with their source information
        return [
            {
                "chunk_id": str(chunk.id),
                "document_id": str(chunk.document_id),
                "filename": filename,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk, filename in chunks
        ]
