from datetime import datetime
from fastapi import APIRouter, HTTPException, Response
from .schemas import ZoneCreate, ZoneUpdate, ZoneOut
from .storage import zones

router = APIRouter(prefix="", tags=["zones"])

#POST /zones
@router.post("/zones", response_model=ZoneOut, status_code=201)
def create_zone(zone: ZoneCreate):
    if zone.id in zones:
        raise HTTPException(status_code=400, detail="Zone id ya existe")

    new_zone = ZoneOut(
        id=zone.id,
        borough=zone.borough,
        zone_name=zone.zone_name,
        service_zone=zone.service_zone,
        active=zone.active,
        created_at=datetime.utcnow()
    )
    zones[zone.id] = new_zone
    return new_zone

# POST /zones/{id}
@router.post("/zones/{zone_id}", response_model=ZoneOut, status_code=201)
def create_zone_with_path_id(zone_id: int, zone: ZoneCreate):
    if zone_id != zone.id:
        raise HTTPException(status_code=400, detail="El id del path debe coincidir con el body")
    return create_zone(zone)

#GET /zones
@router.get("/zones", response_model=list[ZoneOut])
def list_zones(active: bool | None = None, borough: str | None = None):
    data = list(zones.values())

    if active is not None:
        data = [i for i in data if i.active == active]
    if borough is not None:
        data = [i for i in data if i.borough.lower() == borough.lower()]

    return data

# GET /zones/{id}
@router.get("/zones/{zone_id}", response_model=ZoneOut)
def get_zone(zone_id: int):
    if zone_id not in zones:
        raise HTTPException(status_code=404, detail="Zone no encontrada")
    return zones[zone_id]

# PUT /zones/{id}
@router.put("/zones/{zone_id}", response_model=ZoneOut)
def update_zone(zone_id: int, patch: ZoneUpdate):
    if zone_id not in zones:
        raise HTTPException(status_code=404, detail="Zone no encontrada")

    current = zones[zone_id]
    updates = patch.model_dump(exclude_unset=True)

    new_data = current.model_dump()
    new_data.update(updates)

    zones[zone_id] = ZoneOut(**new_data)
    return zones[zone_id]

# DELETE /zones/{id}
@router.delete("/zones/{zone_id}", status_code=204)
def delete_zone(zone_id: int):
    if zone_id not in zones:
        raise HTTPException(status_code=404, detail="Zone no encontrada")
    del zones[zone_id]
    return Response(status_code=204)
