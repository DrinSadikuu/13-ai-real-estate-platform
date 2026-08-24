from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.schemas.client import ClientCreate


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ClientCreate) -> Client:
        client = Client(
            **data.model_dump()
        )

        self.session.add(client)

        await self.session.commit()
        await self.session.refresh(client)

        return client

    async def get_all(self) -> list[Client]:
        result = await self.session.execute(
            select(Client)
        )

        return list(result.scalars().all())

    async def get_by_id(
        self,
        client_id: UUID,
    ) -> Client | None:
        result = await self.session.execute(
            select(Client).where(
                Client.id == client_id
            )
        )

        return result.scalar_one_or_none()

    async def update(self, client: Client, data: ClientCreate) -> Client:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(client, field, value)

        await self.session.commit()
        await self.session.refresh(client)

        return client

    async def deactivate(self, client: Client) -> Client:
        client.is_active = False

        await self.session.commit()
        await self.session.refresh(client)

        return client