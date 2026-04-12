from contextlib import asynccontextmanager

from fastapi import FastAPI
from db import AddHarvestData, Base, GetHarvests, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="GreenhouseCMS",
    lifespan=lifespan,
)

@app.get("/harvests")
def GetMyHarvests():
    AllHarvests = GetHarvests()
    return AllHarvests

@app.post("/harvests")
def AddNewHarvests():
    AddHarvestData()
    return {200}
