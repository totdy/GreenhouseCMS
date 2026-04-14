from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker

from schemas import HarvestPayload, HarvestItem

from models import Harvests

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
    
def UpdateHarvestData(id: int, data: HarvestItem) -> None:
    with session() as new_session:
        update_entry = (
            update(Harvests)
            .filter_by(id = id)
            .values(
                date = data.date,
                plant_type = data.plant_type,
                plant_subtype = data.plant_subtype,
                count = data.count,
                count_unit = data.count_unit,
                unit_price = data.unit_price,
                note = data.note,
            )
        )
        new_session.execute(update_entry)
        new_session.commit()