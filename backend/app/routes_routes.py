from datetime import datetime
from fastapi import APIRouter, HTTPException, Query

from . import storage
from .schemas import RouteCreate, RouteUpdate, RouteOut

router = APIRouter(prefix="/routes", tags=["routes"])


def _validate_route_rules(pickup_id: int, dropoff_id: int):
    if pickup_id == dropoff_id:
        raise HTTPException(status_code=400, detail="pickup_zone_id cannot equal dropoff_zone_id")

    if pickup_id not in storage.zones or dropoff_id not in storage.zones:
        raise HTTPException(status_code=400, detail="pickup_zone_id and/or dropoff_zone_id do not exist in Zones")


@router.post("", response_model=RouteOut, status_code=201)
def create_route(payload: RouteCreate):
    _validate_route_rules(payload.pickup_zone_id, payload.dropoff_zone_id)

    route_id = storage.next_route_id
    storage.next_route_id += 1

    route = RouteOut(
        id=route_id,
        pickup_zone_id=payload.pickup_zone_id,
        dropoff_zone_id=payload.dropoff_zone_id,
        name=payload.name,
        active=payload.active,
        created_at=datetime.utcnow(),
    )
    storage.routes[route_id] = route
    return route


@router.get("", response_model=list[RouteOut])
def list_routes(
    active: bool | None = Query(default=None),
    pickup_zone_id: int | None = Query(default=None, gt=0),
    dropoff_zone_id: int | None = Query(default=None, gt=0),
):
    routes = list(storage.routes.values())

    if active is not None:
        routes = [r for r in routes if r.active == active]
    if pickup_zone_id is not None:
        routes = [r for r in routes if r.pickup_zone_id == pickup_zone_id]
    if dropoff_zone_id is not None:
        routes = [r for r in routes if r.dropoff_zone_id == dropoff_zone_id]

    return routes


@router.get("/{route_id}", response_model=RouteOut)
def get_route(route_id: int):
    if route_id not in storage.routes:
        raise HTTPException(status_code=404, detail="Route not found")
    return storage.routes[route_id]


@router.put("/{route_id}", response_model=RouteOut)
def update_route(route_id: int, payload: RouteUpdate):
    if route_id not in storage.routes:
        raise HTTPException(status_code=404, detail="Route not found")

    current = storage.routes[route_id]

    new_pickup = payload.pickup_zone_id if payload.pickup_zone_id is not None else current.pickup_zone_id
    new_dropoff = payload.dropoff_zone_id if payload.dropoff_zone_id is not None else current.dropoff_zone_id
    new_name = payload.name if payload.name is not None else current.name
    new_active = payload.active if payload.active is not None else current.active

    _validate_route_rules(new_pickup, new_dropoff)

    updated = RouteOut(
        id=current.id,
        pickup_zone_id=new_pickup,
        dropoff_zone_id=new_dropoff,
        name=new_name,
        active=new_active,
        created_at=current.created_at,
    )

    storage.routes[route_id] = updated
    return updated


@router.delete("/{route_id}", status_code=204)
def delete_route(route_id: int):
    if route_id not in storage.routes:
        raise HTTPException(status_code=404, detail="Route not found")
    del storage.routes[route_id]
    return
