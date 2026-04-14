from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from db import AddHarvestData, UpdateHarvestData, GetHarvests, GetHarvestById, engine
from models import Base

from schemas import HarvestPayload, HarvestItem

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
    return GetHarvests()

@app.post("/harvests")
def AddNewHarvests(payload: HarvestPayload):
    AddHarvestData(payload)
    return {"success": True, "inserted": len(payload.data)}

@app.put("/harvests/{id}")
def UpdateMyHarvest(id: int, data: HarvestItem):
    if not GetHarvestById(id):
        raise HTTPException(status_code=404, detail="Harvest not found")
    
    UpdateHarvestData(id, data)
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")