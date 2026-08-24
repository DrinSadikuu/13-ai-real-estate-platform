from pydantic import BaseModel

from app.schemas.property import PropertyResponse


class PropertyMatchResponse(BaseModel):
    property: PropertyResponse
    score: float
    matched: list[str]
    missed: list[str]