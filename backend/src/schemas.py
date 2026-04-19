from datetime import date

from pydantic import BaseModel

class HarvestItem(BaseModel):
    date: date
    plant_type: str
    plant_subtype: str
    count: float
    count_unit: str
    unit_price: float
    note: str = ""

class HarvestPayload(BaseModel):
    data: list[HarvestItem]

class RevenueByDateItem(BaseModel):
    date: date
    revenue: float