from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class ResourceType(str, Enum):
    VIDEO = "Vídeo"
    PDF = "PDF"
    LINK = "Link"


class ResourceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    type: ResourceType
    url: HttpUrl
    tags: Optional[list[str]] = Field(default=None, max_length=3)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    type: Optional[ResourceType] = None
    url: Optional[HttpUrl] = None
    tags: Optional[list[str]] = Field(default=None, max_length=3)


class ResourceOut(ResourceBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedResources(BaseModel):
    items: list[ResourceOut]
    total: int
    page: int

class SmartAssistRequest(BaseModel):
    title: str = Field(..., min_length=1)
    type: ResourceType


class SmartAssistResponse(BaseModel):
    description: str
    tags: list[str]