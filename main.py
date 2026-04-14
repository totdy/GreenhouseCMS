from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import AddHarvestData, Base, GetHarvests, engine

from schemas import HarvestPayload

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
