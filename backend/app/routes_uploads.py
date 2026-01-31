from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from collections import Counter
from datetime import datetime

from . import storage
from .schemas import RouteOut

router = APIRouter(prefix="/uploads", tags=["uploads"])


def _find_existing_route_id(pickup_id: int, dropoff_id: int) -> int | None:
    for rid, r in storage.routes.items():
        # r es RouteOut
        if r.pickup_zone_id == pickup_id and r.dropoff_zone_id == dropoff_id:
            return rid
    return None


@router.post("/parquet")
async def upload_parquet(
    file: UploadFile = File(...),
    top_n: int = Query(default=10, ge=1, le=200),
):
    # Validación básica
    if not file.filename.lower().endswith(".parquet"):
        raise HTTPException(status_code=400, detail="File must be a .parquet")

    # Intentar importar pandas (si no está instalado, devolver error claro)
    try:
        import pandas as pd
        from io import BytesIO
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Missing dependency: install pandas and pyarrow to read parquet",
        )

    data = await file.read()

    # Leer parquet
    try:
        df = pd.read_parquet(BytesIO(data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read parquet: {e}")

    # Detectar columnas típicas (NYC taxi dataset)
    pickup_col = "PULocationID" if "PULocationID" in df.columns else None
    dropoff_col = "DOLocationID" if "DOLocationID" in df.columns else None

    if pickup_col is None or dropoff_col is None:
        raise HTTPException(
            status_code=400,
            detail="Parquet must include PULocationID and DOLocationID columns",
        )

    # Contar pares (pickup, dropoff)
    pairs = list(zip(df[pickup_col].astype(int), df[dropoff_col].astype(int)))
    counts = Counter(pairs)
    top_pairs = counts.most_common(top_n)

    created = 0
    updated = 0
    skipped_missing_zones = 0
    skipped_same_zone = 0

    for (pickup_id, dropoff_id), _cnt in top_pairs:
        if pickup_id == dropoff_id:
            skipped_same_zone += 1
            continue

        # Solo crear/actualizar rutas si existen las zones
        if pickup_id not in storage.zones or dropoff_id not in storage.zones:
            skipped_missing_zones += 1
            continue

        existing_id = _find_existing_route_id(pickup_id, dropoff_id)

        if existing_id is None:
            rid = storage.next_route_id
            storage.next_route_id += 1

            route = RouteOut(
                id=rid,
                pickup_zone_id=pickup_id,
                dropoff_zone_id=dropoff_id,
                name=f"{pickup_id}->{dropoff_id}",
                active=True,
                created_at=datetime.utcnow(),
            )
            storage.routes[rid] = route
            created += 1
        else:
            r = storage.routes[existing_id]
            storage.routes[existing_id] = RouteOut(
                id=r.id,
                pickup_zone_id=r.pickup_zone_id,
                dropoff_zone_id=r.dropoff_zone_id,
                name=r.name,
                active=True,          # “upsert”: la re-activa
                created_at=r.created_at,
            )
            updated += 1

    return {
        "filename": file.filename,
        "rows": int(len(df)),
        "top_n": int(top_n),
        "created_routes": created,
        "updated_routes": updated,
        "skipped_missing_zones": skipped_missing_zones,
        "skipped_same_zone": skipped_same_zone,
    }
