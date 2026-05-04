from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import AddHarvest, UpdateHarvest, GetHarvest, GetRevenueByDate, engine, GetActivityByYear, GetRecentActivity
from src.models import Base

from src.schemas import HarvestPayload, HarvestIn, ActivityPivotResponse, RecentActivityResponse, RevenueByDateResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(
    title="GreenhouseCMS",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/harvests")
def AddNewHarvests(payload: HarvestPayload):
    AddHarvest(payload)
    return {"success": True, "inserted": len(payload.data)}

@app.put("/harvests/{id}")
def UpdateOneHarvest(id: int, payload: HarvestIn):
    if not GetHarvest(id):
        raise HTTPException(status_code=404, detail="Harvest not found")
    UpdateHarvest(id, payload)
    return {"success": True}

@app.get("/harvests/revenue-by-date/{year}", response_model=RevenueByDateResponse)
def GetHarvestRevenueByDate(year: int):
    return {"data": GetRevenueByDate(year=year)}

@app.get("/harvests/activity/{year}", response_model=ActivityPivotResponse)
def GetHarvestActivity(year: int):    
    rows = GetActivityByYear(year=year)

    all_plant_types = []
    for row in rows:
        if row.plant_type not in all_plant_types:
            all_plant_types.append((row.plant_type, row.count_unit))
    all_plant_types = sorted(all_plant_types)

    count_by_month_and_plant = {}
    for row in rows:        
        count_by_month_and_plant[(row.month, row.plant_type)] = row.count

    result_list = []
    for plant in all_plant_types:
        monthly_counts = []
        for month_number in range(1, 13):            
            count = count_by_month_and_plant.get((month_number, plant[0]), 0)
            monthly_counts.append(count)

        plant_entry = {
            "plant_type": plant[0],
            "count": monthly_counts,
            "count_unit": plant[1],
        }
        result_list.append(plant_entry)

    return {"data": result_list}

@app.get("/harvests/recent", response_model=RecentActivityResponse)
def GetLastActivity(limit: int = 10):
    return {"data": GetRecentActivity(limit=min(limit, 50))}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")