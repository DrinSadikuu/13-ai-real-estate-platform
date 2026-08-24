from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    def __init__(self, session: AsyncSession):
        self.repository = ClientRepository(session)

    async def create_client(
        self,
        data: ClientCreate,
    ) -> Client:
        return await self.repository.create(data)

    async def get_clients(self) -> list[Client]:
        return await self.repository.get_all()

    async def get_client_by_id(
        self,
        client_id: UUID,
    ) -> Client:
        client = await self.repository.get_by_id(client_id)

        if client is None:
            raise NotFoundError("Client not found")

        return client

    async def update_client(
            self,
            client: Client,
            data: ClientUpdate,
    ) -> Client:
        return await self.repository.update(
            client,
            data,
        )

    async def deactivate_client(
            self,
            client: Client,
    ) -> Client:
        return await self.repository.deactivate(client)
