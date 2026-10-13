from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.embedding_service import EmbeddingService
from app.core.exceptions import NotFoundError
from app.models.property import Property
from app.repositories.property_repository import PropertyRepository
from app.schemas.property import PropertyCreate, PropertyUpdate


class PropertyService:
    def __init__(self, session: AsyncSession):
        self.repository = PropertyRepository(session)
        self.embedding_service = EmbeddingService()

    async def create_property(self, data: PropertyCreate) -> Property:
        embedding = None

        if data.description:
            embedding = await self.embedding_service.generate_embedding(
                data.description
            )

        return await self.repository.create(
            data,
            embedding=embedding,
        )

    async def get_properties(self) -> list[Property]:
        return await self.repository.get_all()

    async def get_property_by_id(
        self,
        property_id: UUID,
    ) -> Property:
        property_obj = await self.repository.get_by_id(property_id)

        if property_obj is None:
            raise NotFoundError("Property not found")

        return property_obj

    async def update_property(
        self,
        property_obj: Property,
        data: PropertyUpdate,
    ) -> Property:
        return await self.repository.update(
            property_obj,
            data,
        )

    async def deactivate_property(
        self,
        property_obj: Property,
    ) -> Property:
        return await self.repository.deactivate(property_obj)