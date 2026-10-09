from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.client_service import ClientService

async def get_client(
        session: AsyncSession,
        client_is: UUID,
):
    service = ClientService(session)
    return await service.get_client_by_id(client_is)