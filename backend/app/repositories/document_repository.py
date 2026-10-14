
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from sqlalchemy import select, delete


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_document(
        self,
        filename: str,
        s3_key: str,
    ) -> Document:
        document = Document(
            filename=filename,
            s3_key=s3_key,
        )

        self.session.add(document)
        await self.session.flush()

        return document

    async def create_chunks(
        self,
        document_id: UUID,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        for index, (content, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=content,
                embedding=embedding,
            )

            self.session.add(chunk)

        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def search_similar_chunks(
            self,
            query_embedding: list[float],
            limit: int = 5,
            document_id: UUID | None = None,
    ) -> list[tuple[DocumentChunk, str]]:

        stmt = (
            select(DocumentChunk, Document.filename)
            .join(
                Document,
                DocumentChunk.document_id == Document.id,
            )
        )

        if document_id is not None:
            stmt = stmt.where(
                DocumentChunk.document_id == document_id
            )

        stmt = (
            stmt.order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return [
            (chunk, filename)
            for chunk, filename in result.all()
        ]

    async def get_all_documents(self) -> list[Document]:
        stmt = select(Document).order_by(Document.created_at.desc())

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_document_by_id(
            self,
            document_id: UUID,
    ) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete_document(
            self,
            document_id: UUID,
    ) -> bool:
        stmt = (
            delete(Document)
            .where(Document.id == document_id)
            .returning(Document.id)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None


