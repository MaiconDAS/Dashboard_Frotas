from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Setting(Base):
    __tablename__ = "configuracoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chave: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    valor: Mapped[str] = mapped_column(Text, nullable=True)

