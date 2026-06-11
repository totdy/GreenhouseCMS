from contextlib import asynccontextmanager
import math

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import AddHarvest, GetWeeklyActivity, UpdateHarvest, GetHarvest, GetYearlyRevenue, GetMonthlyRevenue, engine, GetYearlyActivity, GetMonthlyActivity, GetHarvestsAll
from src.models import Base

from src.schemas import HarvestPayload, HarvestIn, WeeklyActivityList, YearlyActivityList, MonthlyActivityList, HarvestsAllResponse, YearlyRevenueList, MonthlyRevenueList

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

@app.get("/revenue-by/{year}", response_model=YearlyRevenueList)
def GetRevenueByYear(year: int):
    return {"data": GetYearlyRevenue(year=year)}

@app.get("/revenue-by/{year}/{month}", response_model=MonthlyRevenueList)
def GetRevenueByMonth(year: int, month: int):
    return {"data": GetMonthlyRevenue(year=year,month=month)}

@app.get("/activity/{year}", response_model=YearlyActivityList)
def GetHarvestActivityByYear(year: int):
    return {"data": GetYearlyActivity(year=year)}

@app.get("/activity/{year}/{month}", response_model=MonthlyActivityList)
def GetHarvestActivityByMonth(year: int, month: int):
    return {"data": GetMonthlyActivity(year=year,month=month)}

@app.get("/activity-weekly/{year}", response_model=WeeklyActivityList)
def GetHarvestActivityByWeek(year: int):
    return {"data": GetWeeklyActivity(year=year)}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level="info")
