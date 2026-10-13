from uuid import UUID

from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.schemas.property import PropertyResponse
from app.services.property_service import PropertyService

@tool
async def get_property(property_id: str) -> dict:
    """Retrieve detailed information about a property using its UUID."""
    async with async_session_factory() as session:
        service = PropertyService(session)

        property_obj = await service.get_property_by_id(UUID(property_id))

        return PropertyResponse.model_validate(property_obj).model_dump(mode="json")


@tool
async def get_properties() -> list[dict]:
    """Retrieve all properties available in the real estate database."""

    async with async_session_factory() as session:
        service = PropertyService(session)

        properties = await service.get_properties()
        return [
            PropertyResponse.model_validate(property_obj).model_dump(mode="json")
            for property_obj in properties
        ]

@tool
async def semantic_search_properties(query: str, limit: int = 5) -> list[dict]:
    """Search properties by natural-language descriptions and preferences.

        Use this tool when a user describes the kind of property they want,
        such as a quiet apartment near a park, a family home with a balcony,
        or an office suitable for a business.

        Searches property descriptions using vector embeddings and semantic
        similarity rather than exact keyword matching.
    """
    async with async_session_factory() as session:
        service = PropertyService(session)

        properties = await service.search_properties(
            search_text=query,
            limit=limit,
        )

        return [
            PropertyResponse.model_validate(property_obj).model_dump(mode="json")
            for property_obj in properties
        ]