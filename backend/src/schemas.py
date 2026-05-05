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

class ActivitySeries(BaseModel):
    plant_type: str
    count: list[float]
    count_unit: str

class ActivityPivotResponse(BaseModel):
    data: list[ActivitySeries]

class HarvestsAllResponse(BaseModel):
    data: list[HarvestOut]
    total: int
    page: int
    total_pages: int