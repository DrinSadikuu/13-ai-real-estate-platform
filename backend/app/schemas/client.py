from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ClientCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    notes: str | None = Field(default=None, max_length=5000)

class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    is_active: bool

class ClientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=100)
    last_name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=5000)