from uuid import UUID

from langchain_core.tools import tool

from app.db.database import async_session_factory
from app.schemas.property import PropertyResponse
from app.services.property_matching_service import PropertyMatchingService


@tool
async def find_property_matches_for_client(client_id: str) -> list[dict]:
    """Find property matches for a client using their saved preferences.

    Returns property details, matching scores, and matched/missed criteria.
    """

    async with async_session_factory() as session:
        service = PropertyMatchingService(session)

        matches = await service.find_matches_for_client(UUID(client_id))

        return [
            {
                "property": PropertyResponse.model_validate(
                    match["property"]
                ).model_dump(mode="json"),
                "score": match["score"],
                "matched": match["matched"],
                "missed": match["missed"],
            }
            for match in matches
        ]