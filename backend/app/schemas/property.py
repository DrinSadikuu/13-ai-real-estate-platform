from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PropertyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=5000)

    property_type: str = Field(min_length=2, max_length=50)
    listing_type: str = Field(min_length=2, max_length=20)

    city: str = Field(min_length=2, max_length=100)
    address: str = Field(min_length=3, max_length=255)

    price: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)

    area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    furnished: bool = False


class PropertyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    title: str
    description: str | None

    property_type: str
    listing_type: str

    city: str
    address: str

    price: Decimal

    bedrooms: int | None
    bathrooms: int | None
    area_sqm: Decimal | None

    furnished: bool
    is_active: bool

    created_at: datetime
    updated_at: datetime

class PropertyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=5000)

    property_type: str | None = Field(default=None, min_length=2, max_length=50)
    listing_type: str | None = Field(default=None, min_length=2, max_length=20)

    city: str | None = Field(default=None, min_length=2, max_length=100)
    address: str | None = Field(default=None, min_length=3, max_length=255)

    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)

    area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    furnished: bool | None = None