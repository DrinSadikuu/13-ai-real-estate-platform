from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
)
from app.schemas.property_match import PropertyMatchResponse
from app.services.client_service import ClientService
from app.services.property_matching_service import PropertyMatchingService


router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.post(
    "",
    response_model=ClientResponse,
    status_code=201,
)
async def create_client(
    data: ClientCreate,
    session: AsyncSession = Depends(get_db),
):
    service = ClientService(session)
    return await service.create_client(data)


@router.get(
    "",
    response_model=list[ClientResponse],
)
async def get_clients(
    session: AsyncSession = Depends(get_db),
):
    service = ClientService(session)
    return await service.get_clients()


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
)
async def get_client_by_id(
    client_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = ClientService(session)
    return await service.get_client_by_id(client_id)


@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
)
async def update_client(
    client_id: UUID,
    data: ClientUpdate,
    session: AsyncSession = Depends(get_db),
):
    service = ClientService(session)

    client = await service.get_client_by_id(client_id)

    return await service.update_client(
        client,
        data,
    )


@router.delete(
    "/{client_id}",
    response_model=ClientResponse,
)
async def deactivate_client(
    client_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = ClientService(session)

    client = await service.get_client_by_id(client_id)

    return await service.deactivate_client(client)


@router.get(
    "/{client_id}/property-matches",
    response_model=list[PropertyMatchResponse],
)
async def get_property_matches(
    client_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = PropertyMatchingService(session)

    return await service.find_matches_for_client(client_id)