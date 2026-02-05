from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import func 
from sqlalchemy import ForeignKey, String, Text, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from car_api.models import Base


class Brand(Base):
    __tablename__= 'brands'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String[50], unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    update_at: Mapped[str] = mapped_column(
        onupdate=func.now(), server_default=func.now(),
    )

class Car(Base):
    __tablename__= 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)

    model: Mapped[str] = mapped_column(String[100])
    factory_year: Mapped[int] = mapped_column(Integer)
    model_year: Mapped[int] = mapped_column(Integer)
    color: Mapped[str] = mapped_column(String[30])
    plate: Mapped[str] = mapped_column(String[10], unique=True, index=True)

    price: Mapped[Decimal] = mapped_column(Numeric[10, 2])
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    is_available: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[str] = mapped_column(server_default=func.now())
    update_at: Mapped[str] = mapped_column(
        onupdate=func.now(), server_default=func.now(),
    )
    