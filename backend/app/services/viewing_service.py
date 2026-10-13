from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.models.viewing import Viewing
from app.repositories.client_repository import ClientRepository
from app.repositories.property_repository import PropertyRepository
from app.repositories.viewing_repository import ViewingRepository
from app.schemas.viewing import ViewingCreate, ViewingUpdate


class ViewingService:
    def __init__(self, session: AsyncSession):
        self.viewing_repository = ViewingRepository(session)
        self.client_repository = ClientRepository(session)
        self.property_repository = PropertyRepository(session)

    async def create_viewing(
        self,
        data: ViewingCreate,
    ) -> Viewing:
        client = await self.client_repository.get_by_id(data.client_id)

        if client is None:
            raise NotFoundError("Client not found")

        property_obj = await self.property_repository.get_by_id(
            data.property_id
        )

        if property_obj is None:
            raise NotFoundError("Property not found")

        duplicate = await self.viewing_repository.find_duplicate(
            client_id=data.client_id,
            property_id=data.property_id,
            scheduled_at=data.scheduled_at,
        )

        if duplicate is not None:
            raise ConflictError(
                "A scheduled viewing already exists for this "
                "client, property, and time."
            )

        return await self.viewing_repository.create(data)

    async def get_viewings(
        self,
        client_id: UUID | None = None,
        property_id: UUID | None = None,
    ) -> list[Viewing]:
        return await self.viewing_repository.get_all(
            client_id=client_id,
            property_id=property_id,
        )

    async def get_viewing_by_id(
        self,
        viewing_id: UUID,
    ) -> Viewing:
        viewing = await self.viewing_repository.get_by_id(viewing_id)

        if viewing is None:
            raise NotFoundError("Viewing not found")

        return viewing

    async def update_viewing(
        self,
        viewing: Viewing,
        data: ViewingUpdate,
    ) -> Viewing:
        return await self.viewing_repository.update(
            viewing,
            data,
        )

    async def cancel_viewing(self, viewing: Viewing) -> Viewing:
        return await self.viewing_repository.cancel_viewing(viewing)