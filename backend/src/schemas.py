from datetime import date, datetime

from pydantic import BaseModel

class HarvestIn(BaseModel):
    date: date
    plant_type: str
    count: float
    count_unit: str
    unit_price: float

class HarvestOut(HarvestIn):
    id: int    
    created_at: datetime

class HarvestPayload(BaseModel):
    data: list[HarvestIn]

class RevenueByDateItem(BaseModel):
    date: date
    revenue: float
    
class RevenueByDateResponse(BaseModel):
    data: list[RevenueByDateItem]

class ActivityItem(BaseModel):
    date: date
    count: int

class ActivityResponse(BaseModel):    
    data: list[ActivityItem]

class RecentActivityResponse(BaseModel):
    data: list[HarvestOut]