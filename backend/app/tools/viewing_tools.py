from uuid import UUID

from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.schemas.viewing import ViewingResponse
from app.services.viewing_service import ViewingService


@tool
async def get_viewing(viewing_id: str) -> dict:
    """Retrieve a scheduled property viewing by its UUID."""
    async with async_session_factory() as session:
        service = ViewingService(session)
        viewing = await service.get_viewing_by_id(UUID(viewing_id))

        return ViewingResponse.model_validate(viewing).model_dump(mode="json")


@tool
async def get_viewings(
    client_id: str | None = None,
    property_id: str | None = None,
) -> list[dict]:
    """Retrieve property viewings, optionally filtered by client ID or property ID."""
    async with async_session_factory() as session:
        service = ViewingService(session)

        viewings = await service.get_viewings(
            client_id=UUID(client_id) if client_id else None,
            property_id=UUID(property_id) if property_id else None,
        )

        return [
            ViewingResponse.model_validate(viewing).model_dump(mode="json")
            for viewing in viewings
        ]