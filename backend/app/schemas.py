from datetime import datetime
from pydantic import BaseModel, Field

# -------------------------
# ZONES
# -------------------------
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


# -------------------------
# ROUTES
# -------------------------
class RouteBase(BaseModel):
    pickup_zone_id: int = Field(..., gt=0)
    dropoff_zone_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=3)
    active: bool = True

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    pickup_zone_id: int | None = Field(default=None, gt=0)
    dropoff_zone_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=3)
    active: bool | None = None

class RouteOut(RouteBase):
    id: int
    created_at: datetime
