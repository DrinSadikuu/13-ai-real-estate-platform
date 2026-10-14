from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.services.document_service import DocumentService
from uuid import UUID


@tool
async def search_property_documents(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
) -> list[dict]:
    """Search uploaded PDF documents using semantic similarity.

    Use this tool when the user asks about information in uploaded
    property documents, rental conditions, deposits, contracts,
    property rules, or viewing instructions.

    If a document UUID is provided, search only that document.
    Otherwise, search across all uploaded documents.
    """

    async with async_session_factory() as session:
        service = DocumentService(session)

        return await service.search_documents(
            query=query,
            limit=limit,
            document_id=UUID(document_id) if document_id else None,
        )