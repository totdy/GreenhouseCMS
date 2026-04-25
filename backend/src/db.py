from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import sessionmaker

from src.schemas import HarvestPayload, HarvestItem, RevenueByDateItem

from src.models import Harvests

engine = create_engine(url="sqlite:///greenhouse.db")

session = sessionmaker(engine)

def GetHarvests() -> list[Harvests]:
    with session() as new_session:
        query = select(Harvests)
        result = new_session.execute(query)
        return result.scalars().all() # type: ignore
    
def GetHarvestById(id: int) -> Harvests | None:
    with session() as new_session:
        query = select(Harvests).filter_by(id = id)
        result = new_session.execute(query)
        return result.scalars().first() # type: ignore

def AddHarvestData(payload: HarvestPayload) -> None:
    with session() as new_session:
        for item in payload.data:
            new_entry = Harvests(
                date = item.date,
                plant_type = item.plant_type,
                plant_subtype = item.plant_subtype,
                count = item.count,
                count_unit = item.count_unit,
                unit_price = item.unit_price,
                note = item.note,
            )
            new_session.add(new_entry)
        new_session.commit()
    
def UpdateHarvestData(id: int, payload: HarvestItem) -> None:
    with session() as new_session:
        update_entry = (
            update(Harvests)
            .filter_by(id = id)
            .values(
                date = payload.date,
                plant_type = payload.plant_type,
                plant_subtype = payload.plant_subtype,
                count = payload.count,
                count_unit = payload.count_unit,
                unit_price = payload.unit_price,
                note = payload.note,
            )
        )
        new_session.execute(update_entry)
        new_session.commit()

def GetRevenueByDate(year: int) -> list[RevenueByDateItem]:
    with session() as new_session:
        query = (
            select(
                Harvests.date,
                func.round(func.sum(Harvests.count * Harvests.unit_price), 2).label("revenue"),
            )
            .filter(Harvests.date.between(f"{year}-01-01", f"{year}-12-31"))
            .group_by(Harvests.date)
            .order_by(Harvests.date)
        )
        result = new_session.execute(query)
        return result.all() # type: ignore