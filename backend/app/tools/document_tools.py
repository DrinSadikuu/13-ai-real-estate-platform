from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.services.document_service import DocumentService


@tool
async def search_property_documents(
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Search uploaded PDF documents for real estate information.

    Use this tool when the user asks questions about uploaded
    property documents, rental conditions, deposits, contracts,
    property rules, or viewing instructions.
    """

    async with async_session_factory() as session:
        service = DocumentService(session)

        return await service.search_documents(
            query=query,
            limit=limit,
        )