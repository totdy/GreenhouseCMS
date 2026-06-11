from datetime import date, datetime
from pydantic import BaseModel

class HarvestIn(BaseModel):
    date: date
    plant_type: str
    count: float
    unit_price: float

class HarvestOut(HarvestIn):
    id: int
    created_at: datetime

class HarvestPayload(BaseModel):
    data: list[HarvestIn]

class YearlyRevenueItem(BaseModel):
    month: int
    revenue: float

class YearlyRevenueList(BaseModel):
    data: list[YearlyRevenueItem]

class YearlyActivityItem(BaseModel):
    month: int
    plant_type: str
    count: float

class YearlyActivityList(BaseModel):
    data: list[YearlyActivityItem]

class HarvestsAllResponse(BaseModel):
    data: list[HarvestOut]
    total: int
    page: int
    total_pages: int

class MonthlyRevenueItem(BaseModel):
    date: date
    revenue: float

class MonthlyRevenueList(BaseModel):
    data: list[MonthlyRevenueItem]

class MonthlyActivityItem(BaseModel):
    date: date
    plant_type: str
    count: float

class MonthlyActivityList(BaseModel):
    data: list[MonthlyActivityItem]

class WeeklyActivityItem(BaseModel):
    week: int
    plant_type: str
    count: float

class WeeklyActivityList(BaseModel):
    data: list[WeeklyActivityItem]