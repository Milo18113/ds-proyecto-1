from fastapi import FastAPI
from .routes_zones import router as zones_router

app = FastAPI(title="Demand Prediction Service - PSet #1")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(zones_router)
