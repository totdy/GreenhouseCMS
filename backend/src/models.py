from datetime import datetime, date, timezone

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Harvests(Base):
    __tablename__ = "harvests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)    
    plant_type: Mapped[str] = mapped_column(String)
    count: Mapped[float] = mapped_column(Numeric(10, 2))
    count_unit: Mapped[str] = mapped_column(String)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
