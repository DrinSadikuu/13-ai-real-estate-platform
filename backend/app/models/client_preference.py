from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ClientPreference(Base):
    __tablename__ = "client_preferences"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    client_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("clients.id"),
        nullable=False,
        unique=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    property_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    listing_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    max_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    min_bedrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    min_bathrooms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    min_area_sqm: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    furnished: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )