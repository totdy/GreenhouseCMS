from datetime import datetime, date, timezone

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase

from schemas import HarvestPayload

engine = create_engine(url="sqlite:///greenhouse.db")

session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Harvests(Base):
    __tablename__ = "harvests"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)    
    plant_type: Mapped[str] = mapped_column(String)
    plant_subtype: Mapped[str] = mapped_column(String)
    count: Mapped[float] = mapped_column(Numeric(10, 2))
    count_unit: Mapped[str] = mapped_column(String)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 4))
    note: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))



def AddHarvestData(payload: HarvestPayload) -> None:
    with session() as new_session:
        for item in payload.data:
            new_entry = Harvests(
                date=item.date,                
                plant_type=item.plant_type,
                plant_subtype=item.plant_subtype,
                count=item.count,
                count_unit=item.count_unit,
                unit_price=item.unit_price,
                note=item.note,
            )
            new_session.add(new_entry)
        new_session.commit()

def GetHarvests() -> list[Harvests]:
    with session() as new_session:
        query = select(Harvests)
        result = new_session.execute(query)
        return result.scalars().all() # type: ignore