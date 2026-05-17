from sqlalchemy import create_engine, extract, select, update, func
from sqlalchemy.orm import sessionmaker

from src.schemas import HarvestPayload, HarvestIn, YearlyActivityItem, YearlyRevenueItem, HarvestOut, MonthlyRevenueItem, MonthlyActivityItem

from src.models import Harvests

import calendar

engine = create_engine(url="sqlite:///greenhouse.db")

session = sessionmaker(engine)

def GetHarvest(id: int) -> Harvests | None:
    with session() as new_session:
        query = select(Harvests).filter_by(id = id)
        result = new_session.execute(query)
        return result.scalars().first() # type: ignore

def AddHarvest(payload: HarvestPayload) -> None:
    with session() as new_session:
        for item in payload.data:
            new_entry = Harvests(
                date = item.date,
                plant_type = item.plant_type,
                count = item.count,
                unit_price = item.unit_price,
            )
            new_session.add(new_entry)
        new_session.commit()
    
def UpdateHarvest(id: int, payload: HarvestIn) -> None:
    with session() as new_session:
        update_entry = (
            update(Harvests)
            .filter_by(id = id)
            .values(
                date = payload.date,
                plant_type = payload.plant_type,
                count = payload.count,
                unit_price = payload.unit_price,
            )
        )
        new_session.execute(update_entry)
        new_session.commit()

def GetHarvestsAll(page: int = 1) -> tuple[list[HarvestOut], int]:
    with session() as new_session:
        total: int = new_session.execute(select(func.count()).select_from(Harvests)).scalar_one()

        query = (
            select(Harvests)
            .order_by(Harvests.created_at.desc())
            .offset((page - 1) * 15)
            .limit(15)
        )
        result = new_session.execute(query)
        rows = result.scalars().all() # type: ignore
        return rows, total # type: ignore

def GetYearlyRevenue(year: int) -> list[YearlyRevenueItem]:
    with session() as new_session:
        query = (
            select(
                extract('month', Harvests.date).label("month"),
                func.round(func.sum(Harvests.count * Harvests.unit_price), 2).label("revenue")
            )
            .filter(Harvests.date.between(f"{year}-01-01", f"{year}-12-31"))
            .group_by(extract('month', Harvests.date))
            .order_by(extract('month', Harvests.date))
        )
        result = new_session.execute(query)
        return result.all() # type: ignore

def GetMonthlyRevenue(year: int, month: int) -> list[MonthlyRevenueItem]:
    with session() as new_session:
        last_day = calendar.monthrange(year, month)[1]
        query = (
            select(
                Harvests.date,
                func.round(func.sum(Harvests.count * Harvests.unit_price), 2).label("revenue")
            )
            .filter(Harvests.date.between(f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day:02d}"))
            .group_by(Harvests.date)
            .order_by(Harvests.date)
        )
        result = new_session.execute(query)
        return result.all() # type: ignore

def GetYearlyActivity(year: int) -> list[YearlyActivityItem]:
    with session() as new_session:
        query = (
            select(
                extract('month', Harvests.date).label("month"),
                Harvests.plant_type,
                func.sum(Harvests.count).label("count")
            )
            .filter(Harvests.date.between(f"{year}-01-01", f"{year}-12-31"))
            .group_by(extract('month', Harvests.date), Harvests.plant_type)
            .order_by(extract('month', Harvests.date))
        )
        result = new_session.execute(query)
        return result.all() # type: ignore

def GetMonthlyActivity(year: int, month: int) -> list[MonthlyActivityItem]:
    with session() as new_session:
        last_day = calendar.monthrange(year, month)[1]
        query = (
            select(
                Harvests.date,
                Harvests.plant_type,
                func.sum(Harvests.count).label("count")
            )
            .filter(Harvests.date.between(f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day:02d}"))
            .group_by(Harvests.date, Harvests.plant_type)
            .order_by(Harvests.date)
        )
        result = new_session.execute(query)
        return result.all() # type: ignore