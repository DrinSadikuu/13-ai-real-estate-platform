from fastapi import APIRouter, HTTPException, Request

from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
    AgentApprovalRequest,
)

from app.services.agent_service import AgentService


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


@router.post(
    "/chat",
    response_model=AgentResponse,
)
async def chat_with_agent(data: AgentRequest, request: Request):
    service = AgentService(request.app.state.graph)

    try:
        result = await service.run(
            message=data.message,
            thread_id=data.thread_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return AgentResponse(**result)


@router.post(
    "/approve",
    response_model=AgentResponse,
)
async def approve_agent_action(data: AgentApprovalRequest, request: Request):
    service = AgentService(request.app.state.graph)

    try:
        result = await service.approve(data.thread_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return AgentResponse(**result)

@router.post(
    "/reject",
    response_model=AgentResponse,
)
async def reject_agent_action(data: AgentApprovalRequest, request: Request):
    service = AgentService(request.app.state.graph)
    try:
        result = await service.reject(data.thread_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return AgentResponse(**result)
