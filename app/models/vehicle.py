from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, Text, func, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Vehicle(Base):
    __tablename__ = "veiculos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    modelo: Mapped[str] = mapped_column(String(80), nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(80))
    ano: Mapped[Optional[int]] = mapped_column(Integer)
    categoria: Mapped[str] = mapped_column(String(20), nullable=False, default="Outros")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Ativo")
    observacoes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.current_timestamp())

    activities: Mapped[List["Activity"]] = relationship(
        back_populates="vehicle", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("categoria IN ('Carga Pesada','Carga Leve','Outros')", name="ck_veiculos_categoria"),
        CheckConstraint("status IN ('Ativo','Inativo','Em Manutenção')", name="ck_veiculos_status"),
        Index("ix_veiculos_categoria_status", "categoria", "status"),
    )

