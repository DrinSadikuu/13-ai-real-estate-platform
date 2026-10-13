from typing import Any

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str
    thread_id: str | None = None


class PendingAction(BaseModel):
    name: str
    args: dict[str, Any]
    id: str | None = None


class AgentResponse(BaseModel):
    thread_id: str
    status: str
    response: str
    pending_actions: list[PendingAction] = Field(default_factory=list)


class AgentApprovalRequest(BaseModel):
    thread_id: str