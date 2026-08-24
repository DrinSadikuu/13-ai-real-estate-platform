from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.client_preference import ClientPreference
from app.repositories.client_preference_repository import ClientPreferenceRepository
from app.repositories.client_repository import ClientRepository
from app.schemas.client_preference import (
    ClientPreferenceCreate,
    ClientPreferenceUpdate,
)


class ClientPreferenceService:
    def __init__(self, session: AsyncSession):
        self.preference_repository = ClientPreferenceRepository(session)
        self.client_repository = ClientRepository(session)

    async def create_preference(
        self,
        data: ClientPreferenceCreate,
    ) -> ClientPreference:
        client = await self.client_repository.get_by_id(data.client_id)

        if client is None:
            raise NotFoundError("Client not found")

        existing_preference = await self.preference_repository.get_by_client_id(
            data.client_id
        )

        if existing_preference is not None:
            raise ValueError("Client already has a preference profile")

        return await self.preference_repository.create(data)

    async def get_preference_by_client_id(
        self,
        client_id: UUID,
    ) -> ClientPreference:
        preference = await self.preference_repository.get_by_client_id(client_id)

        if preference is None:
            raise NotFoundError("Client preference not found")

        return preference

    async def update_preference(
        self,
        preference: ClientPreference,
        data: ClientPreferenceUpdate,
    ) -> ClientPreference:
        return await self.preference_repository.update(
            preference,
            data,
        )