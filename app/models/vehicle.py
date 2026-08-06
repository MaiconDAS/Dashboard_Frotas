from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.activity import Activity


class Vehicle(Base):
    __tablename__ = "veiculos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    modelo: Mapped[Optional[str]] = mapped_column(String(80))
    marca: Mapped[Optional[str]] = mapped_column(String(80))
    ano: Mapped[Optional[int]]
    categoria: Mapped[Optional[str]] = mapped_column(String(20))
    status: Mapped[Optional[str]] = mapped_column(String(20))
    observacoes: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="vehicle", cascade="all, delete-orphan"
    )
