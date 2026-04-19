from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import AddHarvestData, UpdateHarvestData, GetHarvests, GetHarvestById, GetRevenueByDate, engine
from src.models import Base

from src.schemas import HarvestPayload, HarvestItem, RevenueByDateItem

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="GreenhouseCMS",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/harvests")
def GetMyHarvests():
    return {"data": GetHarvests()}

@app.get("/harvests/revenue-by-date")
def GetHarvestRevenueByDate():
    rows = GetRevenueByDate()
    return {"data": [RevenueByDateItem(date=row.date, revenue=row.revenue) for row in rows]}

@app.post("/harvests")
def AddNewHarvests(payload: HarvestPayload):
    AddHarvestData(payload)
    return {"success": True, "inserted": len(payload.data)}

@app.put("/harvests/{id}")
def UpdateMyHarvest(id: int, payload: HarvestItem):
    if not GetHarvestById(id):
        raise HTTPException(status_code=404, detail="Harvest not found")
    
    UpdateHarvestData(id, payload)
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")