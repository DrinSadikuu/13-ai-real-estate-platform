from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_preference import ClientPreference
from app.schemas.client_preference import (
    ClientPreferenceCreate,
    ClientPreferenceUpdate,
)
from decimal import Decimal
from app.models.property import Property


class ClientPreferenceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: ClientPreferenceCreate,
    ) -> ClientPreference:
        preference = ClientPreference(
            **data.model_dump()
        )

        self.session.add(preference)

        await self.session.commit()
        await self.session.refresh(preference)

        return preference

    async def get_by_client_id(
        self,
        client_id: UUID,
    ) -> ClientPreference | None:
        result = await self.session.execute(
            select(ClientPreference).where(
                ClientPreference.client_id == client_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        preference: ClientPreference,
        data: ClientPreferenceUpdate,
    ) -> ClientPreference:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(preference, field, value)

        await self.session.commit()
        await self.session.refresh(preference)

        return preference

    async def find_matches(
            self,
            city: str | None = None,
            property_type: str | None = None,
            listing_type: str | None = None,
            max_price: Decimal | None = None,
            min_bedrooms: int | None = None,
            min_bathrooms: int | None = None,
            min_area_sqm: Decimal | None = None,
            furnished: bool | None = None,
    ) -> list[Property]:
        query = select(Property).where(
            Property.is_active.is_(True)
        )

        if city is not None:
            query = query.where(Property.city == city)

        if property_type is not None:
            query = query.where(
                Property.property_type == property_type
            )

        if listing_type is not None:
            query = query.where(
                Property.listing_type == listing_type
            )

        if max_price is not None:
            query = query.where(
                Property.price <= max_price
            )

        if min_bedrooms is not None:
            query = query.where(
                Property.bedrooms >= min_bedrooms
            )

        if min_bathrooms is not None:
            query = query.where(
                Property.bathrooms >= min_bathrooms
            )

        if min_area_sqm is not None:
            query = query.where(
                Property.area_sqm >= min_area_sqm
            )

        if furnished is not None:
            query = query.where(
                Property.furnished == furnished
            )

        result = await self.session.execute(query)

        return list(result.scalars().all())