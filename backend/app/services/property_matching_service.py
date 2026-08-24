from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories.client_preference_repository import ClientPreferenceRepository
from app.repositories.property_repository import PropertyRepository


class PropertyMatchingService:
    def __init__(self, session: AsyncSession):
        self.preference_repository = ClientPreferenceRepository(session)
        self.property_repository = PropertyRepository(session)

    async def find_matches_for_client(
        self,
        client_id: UUID,
    ) -> list[dict]:
        preference = await self.preference_repository.get_by_client_id(
            client_id
        )

        if preference is None:
            raise NotFoundError("Client preference not found")

        properties = await self.property_repository.get_all()

        matches = []

        for property_obj in properties:
            if not property_obj.is_active:
                continue

            score = 0
            matched = []
            missed = []

            if preference.city is None or property_obj.city == preference.city:
                score += 20
                matched.append("city")
            else:
                missed.append("city")

            if (
                preference.property_type is None
                or property_obj.property_type == preference.property_type
            ):
                score += 15
                matched.append("property_type")
            else:
                missed.append("property_type")

            if (
                preference.listing_type is None
                or property_obj.listing_type == preference.listing_type
            ):
                score += 15
                matched.append("listing_type")
            else:
                missed.append("listing_type")

            if (
                preference.max_price is None
                or property_obj.price <= preference.max_price
            ):
                score += 20
                matched.append("price")
            else:
                missed.append("price")

            if (
                preference.min_bedrooms is None
                or (
                    property_obj.bedrooms is not None
                    and property_obj.bedrooms >= preference.min_bedrooms
                )
            ):
                score += 10
                matched.append("bedrooms")
            else:
                missed.append("bedrooms")

            if (
                preference.min_bathrooms is None
                or (
                    property_obj.bathrooms is not None
                    and property_obj.bathrooms >= preference.min_bathrooms
                )
            ):
                score += 5
                matched.append("bathrooms")
            else:
                missed.append("bathrooms")

            if (
                preference.min_area_sqm is None
                or (
                    property_obj.area_sqm is not None
                    and property_obj.area_sqm >= preference.min_area_sqm
                )
            ):
                score += 10
                matched.append("area")
            else:
                missed.append("area")

            if (
                preference.furnished is None
                or property_obj.furnished == preference.furnished
            ):
                score += 5
                matched.append("furnished")
            else:
                missed.append("furnished")

            matches.append(
                {
                    "property": property_obj,
                    "score": float(score),
                    "matched": matched,
                    "missed": missed,
                }
            )

        matches.sort(
            key=lambda match: match["score"],
            reverse=True,
        )

        return matches