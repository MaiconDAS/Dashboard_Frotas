from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.models.base import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    nome_completo = Column(String(100), nullable=False)
    is_master = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
