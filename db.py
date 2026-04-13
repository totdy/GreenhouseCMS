from datetime import datetime, date, timezone

from sqlalchemy import Date, DateTime, Integer, Numeric, Sequence, String, Text, create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase

engine = create_engine(url="sqlite:///greenhouse.db")

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass

class Harvests(Base):
    __tablename__ = "harvests"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    zone: Mapped[str] = mapped_column(String)
    plant_type: Mapped[str] = mapped_column(String)
    plant_subtype: Mapped[str] = mapped_column(String)
    count: Mapped[float] = mapped_column(Numeric(10, 2))
    count_unit: Mapped[str] = mapped_column(String)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 4))
    note: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

def AddHarvestData () -> None:
    with session() as new_session:
        new_request = Harvests(
            date = date.today(),
            zone = "G1",
            plant_type = "tomato",
            plant_subtype = "cherry",
            count = 0.0,
            count_unit = "kg",
            unit_price = 0.0,
            note = "",
        )

        new_session.add(new_request)
        new_session.commit()

def GetHarvests() -> list[Harvests]:
    with session() as new_session:
        query = select(Harvests)
        result = new_session.execute(query)
        return result.scalars().all()