from uuid import UUID
from datetime import datetime

from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.schemas.viewing import ViewingCreate, ViewingResponse
from app.services.viewing_service import ViewingService


@tool
async def schedule_viewing(
    client_id: str,
    property_id: str,
    scheduled_at: datetime,
    notes: str | None = None,
) -> dict:
    """Schedule a property viewing for an existing client and property.

    Args:
        client_id: UUID of the client.
        property_id: UUID of the property.
        scheduled_at: Viewing date and time, including timezone.
        notes: Optional notes about the viewing.
    """

    data = ViewingCreate(
        client_id=UUID(client_id),
        property_id=UUID(property_id),
        scheduled_at=scheduled_at,
        notes=notes,
    )

    async with async_session_factory() as session:
        service = ViewingService(session)

        viewing = await service.create_viewing(data)

        return ViewingResponse.model_validate(viewing).model_dump(mode="json")