from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.client_preference import (
    ClientPreferenceCreate,
    ClientPreferenceResponse,
    ClientPreferenceUpdate,
)
from app.services.client_preference_service import ClientPreferenceService

router = APIRouter(
    prefix="/client-preferences",
    tags=["client-preferences"],
)

@router.post(
    "",
    response_model=ClientPreferenceResponse,
    status_code=201,
)
async def create_preference(
    data: ClientPreferenceCreate,
    session: AsyncSession = Depends(get_db),
):
    service = ClientPreferenceService(session)
    return await service.create_preference(data)

@router.get(
    "/{client_id}",
    response_model=ClientPreferenceResponse,
)
async def get_preference(
    client_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = ClientPreferenceService(session)

    return await service.get_preference_by_client_id(client_id)

@router.patch(
    "/{client_id}",
    response_model=ClientPreferenceResponse,
)
async def update_preference(
    client_id: UUID,
    data: ClientPreferenceUpdate,
    session: AsyncSession = Depends(get_db),
):
    service = ClientPreferenceService(session)

    preference = await service.get_preference_by_client_id(client_id)

    return await service.update_preference(
        preference,
        data,
    )