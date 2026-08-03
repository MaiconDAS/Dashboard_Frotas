from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Activity(Base):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    veiculo_id: Mapped[int] = mapped_column(ForeignKey("veiculos.id"), nullable=False, index=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    observacoes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())

    vehicle = relationship("Vehicle", back_populates="activities")

    __table_args__ = (
        Index("ix_atividades_veiculo_data", "veiculo_id", "data_hora"),
    )
