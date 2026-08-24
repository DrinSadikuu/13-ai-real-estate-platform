from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClientPreferenceCreate(BaseModel):
    client_id: UUID

    city: str | None = Field(default=None, min_length=2, max_length=100)
    property_type: str | None = Field(default=None, min_length=2, max_length=50)
    listing_type: str | None = Field(default=None, min_length=2, max_length=20)

    max_price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    min_bedrooms: int | None = Field(default=None, ge=0)
    min_bathrooms: int | None = Field(default=None, ge=0)

    min_area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    furnished: bool | None = None


class ClientPreferenceUpdate(BaseModel):
    city: str | None = Field(default=None, min_length=2, max_length=100)
    property_type: str | None = Field(default=None, min_length=2, max_length=50)
    listing_type: str | None = Field(default=None, min_length=2, max_length=20)

    max_price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    min_bedrooms: int | None = Field(default=None, ge=0)
    min_bathrooms: int | None = Field(default=None, ge=0)

    min_area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    furnished: bool | None = None


class ClientPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_id: UUID
    city: str | None
    property_type: str | None
    listing_type: str | None
    max_price: Decimal | None
    min_bedrooms: int | None
    min_bathrooms: int | None
    min_area_sqm: Decimal | None
    furnished: bool | None