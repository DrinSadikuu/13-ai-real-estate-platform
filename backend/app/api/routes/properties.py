from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.property import (
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
)
from app.services.property_service import PropertyService


router = APIRouter(
    prefix="/properties",
    tags=["properties"],
)


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=201,
)
async def create_property(
    data: PropertyCreate,
    session: AsyncSession = Depends(get_db),
):
    service = PropertyService(session)
    return await service.create_property(data)


@router.get(
    "",
    response_model=list[PropertyResponse],
)
async def get_properties(
    session: AsyncSession = Depends(get_db),
):
    service = PropertyService(session)
    return await service.get_properties()


@router.get(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def get_property_by_id(
    property_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = PropertyService(session)

    property_obj = await service.get_property_by_id(property_id)

    return property_obj

@router.patch(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def update_property(
    property_id: UUID,
    data: PropertyUpdate,
    session: AsyncSession = Depends(get_db),
):
    service = PropertyService(session)

    property_obj = await service.get_property_by_id(property_id)

    return await service.update_property(
        property_obj,
        data,
    )

@router.delete(
    "/{property_id}",
    response_model=PropertyResponse,
)
async def deactivate_property(
    property_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = PropertyService(session)

    property_obj = await service.get_property_by_id(property_id)


    return await service.deactivate_property(property_obj)