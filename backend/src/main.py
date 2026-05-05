from contextlib import asynccontextmanager
import math

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import AddHarvest, UpdateHarvest, GetHarvest, GetRevenueByDate, engine, GetActivityByYear, GetHarvestsAll
from src.models import Base

from src.schemas import HarvestPayload, HarvestIn, ActivityPivotResponse, HarvestsAllResponse, RevenueByDateResponse

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

@app.get("/harvests/all/{page}", response_model=HarvestsAllResponse)
def GetAllActivity(page: int = 1):
    rows, total = GetHarvestsAll(page=page)
    return {
        "data": rows,
        "total": total,
        "page": page,
        "total_pages": math.ceil(total / 15) if total else 1,
    }

@app.get("/revenue-by-date/{year}", response_model=RevenueByDateResponse)
def GetHarvestRevenueByDate(year: int):
    return {"data": GetRevenueByDate(year=year)}

@app.get("/activity/{year}", response_model=ActivityPivotResponse)
def GetHarvestActivity(year: int):    
    rows = GetActivityByYear(year=year)

    all_plant_types = []
    seen = set()
    for row in rows:
        if row.plant_type not in seen:
            seen.add(row.plant_type)
            all_plant_types.append((row.plant_type, row.count_unit))
    all_plant_types = sorted(all_plant_types)

    count_by_month_and_plant = {}
    for row in rows:        
        count_by_month_and_plant[(row.month, row.plant_type)] = row.count

    result_list = []
    for (plant, unit) in all_plant_types:
        monthly_counts = []
        for month_number in range(1, 13):            
            count = count_by_month_and_plant.get((month_number, plant), 0)
            monthly_counts.append(count)

        plant_entry = {
            "plant_type": plant,
            "count": monthly_counts,
            "count_unit": unit,
        }
        result_list.append(plant_entry)

    return {"data": result_list}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")