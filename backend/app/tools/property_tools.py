from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.property_service import PropertyService


async def get_property(
    session: AsyncSession,
    property_id: UUID,
):
    service = PropertyService(session)
    return await service.get_property_by_id(property_id)


async def get_properties(
    session: AsyncSession,
):
    service = PropertyService(session)
    return await service.get_properties()