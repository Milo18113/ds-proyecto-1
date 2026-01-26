from datetime import datetime
from pydantic import BaseModel, Field

class ZoneBase(BaseModel):
    borough: str = Field(..., min_length=1)
    zone_name: str = Field(..., min_length=1)
    service_zone: str = Field(..., min_length=1)
    active: bool = True

class ZoneCreate(ZoneBase):
    id: int = Field(..., gt=0)

class ZoneUpdate(BaseModel):
    borough: str | None = Field(default=None, min_length=1)
    zone_name: str | None = Field(default=None, min_length=1)
    service_zone: str | None = Field(default=None, min_length=1)
    active: bool | None = None

class ZoneOut(ZoneBase):
    id: int
    created_at: datetime
