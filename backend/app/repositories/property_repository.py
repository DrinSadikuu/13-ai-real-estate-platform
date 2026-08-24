from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate



class PropertyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PropertyCreate) -> Property:
        property_obj = Property(
            **data.model_dump()
        )

        self.session.add(property_obj)

        await self.session.commit()
        await self.session.refresh(property_obj)

        return property_obj

    async def get_all(self) -> list[Property]:
        result = await self.session.execute(
            select(Property)
        )

        return list(result.scalars().all())

    async def get_by_id(self, property_id: UUID) -> Property | None:
        result = await self.session.execute(
            select(Property).where(
                Property.id == property_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
            self,
            property_obj: Property,
            data: PropertyUpdate,
    ) -> Property:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(property_obj, field, value)

        await self.session.commit()
        await self.session.refresh(property_obj)

        return property_obj

    async def deactivate(
            self,
            property_obj: Property,
    ) -> Property:
        property_obj.is_active = False

        await self.session.commit()
        await self.session.refresh(property_obj)

        return property_obj

