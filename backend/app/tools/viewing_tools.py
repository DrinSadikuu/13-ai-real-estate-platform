from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.viewing_service import ViewingService

async def get_viewing(
    session: AsyncSession,
    viewing_id: UUID,
):
    service = ViewingService(session)
    return await service.get_viewing_by_id(viewing_id)

async def get_viewings(
    session: AsyncSession,
    client_id: UUID | None = None,
    property_id: UUID | None = None,
):
    service = ViewingService(session)

    return await service.get_viewings(
        client_id=client_id,
        property_id=property_id,
    )