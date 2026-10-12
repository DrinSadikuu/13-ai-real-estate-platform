from uuid import UUID

from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.schemas.client import ClientResponse
from app.services.client_service import ClientService


@tool
async def get_client(client_id: str) -> dict:
    """Retrieve a real estate client's details by their UUID."""

    async with async_session_factory() as session:
        service = ClientService(session)

        client = await service.get_client_by_id(UUID(client_id))

        return ClientResponse.model_validate(client).model_dump(mode="json")