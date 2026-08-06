from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle


class Activity(Base):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    veiculo_id: Mapped[int] = mapped_column(ForeignKey("veiculos.id"), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(nullable=False)
    quantidade: Mapped[int] = mapped_column(default=1)
    observacoes: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="activities")
