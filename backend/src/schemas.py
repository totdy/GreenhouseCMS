from datetime import date

from pydantic import BaseModel

class HarvestItem(BaseModel):
    date: date
    plant_type: str
    count: float
    count_unit: str
    unit_price: float

class HarvestPayload(BaseModel):
    data: list[HarvestItem]

class RevenueByDateItem(BaseModel):
    date: date
    revenue: float