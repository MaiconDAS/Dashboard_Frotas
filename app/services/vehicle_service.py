from __future__ import annotations

import logging
import re
from typing import List

from app.core.database import session_scope
from app.models.vehicle import Vehicle

logger = logging.getLogger(__name__)

_PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
_PLACA_ANTIGA = re.compile(r"^[A-Z]{3}-?[0-9]{4}$")


def validar_placa(placa: str) -> bool:
    p = placa.strip().upper().replace("-", "")
    return bool(_PLACA_MERCOSUL.match(p) or _PLACA_ANTIGA.match(p))


def normalize_plate(placa: str) -> str:
    p = placa.strip().upper().replace("-", "")
    if _PLACA_ANTIGA.match(p) and len(p) == 7:
        return f"{p[:3]}-{p[3:]}"
    return p


class VehicleService:
    @staticmethod
    def create(
        *,
        placa: str,
        modelo: str | None = None,
        marca: str | None = None,
        ano: int | None = None,
        categoria: str = "Outros",
        status: str = "Ativo",
        observacoes: str | None = None,
    ) -> dict:
        placa = normalize_plate(placa)
        if not validar_placa(placa):
            raise ValueError("Placa invalida.")

        with session_scope() as session:
            existing = session.query(Vehicle).filter_by(placa=placa).first()
            if existing:
                raise ValueError(f"Placa '{placa}' ja cadastrada.")

            v = Vehicle(
                placa=placa,
                modelo=modelo or placa,
                marca=marca,
                ano=ano,
                categoria=categoria,
                status=status,
                observacoes=observacoes,
            )
            session.add(v)
            session.flush()
            session.refresh(v)
            return _to_dict(v)

    @staticmethod
    def update(vehicle_id: int, **kwargs) -> dict:
        with session_scope() as session:
            v = session.get(Vehicle, vehicle_id)
            if not v:
                raise ValueError("Veiculo nao encontrado.")

            if "placa" in kwargs:
                kwargs["placa"] = normalize_plate(kwargs["placa"])
                if not validar_placa(kwargs["placa"]):
                    raise ValueError("Placa invalida.")

            for key, value in kwargs.items():
                if hasattr(v, key):
                    setattr(v, key, value)

            session.flush()
            session.refresh(v)
            return _to_dict(v)

    @staticmethod
    def delete(vehicle_id: int) -> None:
        with session_scope() as session:
            v = session.get(Vehicle, vehicle_id)
            if not v:
                raise ValueError("Veiculo nao encontrado.")
            session.delete(v)

    @staticmethod
    def list(search: str = "") -> List[dict]:
        with session_scope() as session:
            query = session.query(Vehicle)
            if search:
                s = f"%{search}%"
                query = query.filter(
                    (Vehicle.placa.ilike(s)) |
                    (Vehicle.modelo.ilike(s)) |
                    (Vehicle.categoria.ilike(s))
                )
            query = query.order_by(Vehicle.placa)
            return [_to_dict(v) for v in query.all()]


def _to_dict(v: Vehicle) -> dict:
    return {
        "id": v.id,
        "placa": v.placa,
        "modelo": v.modelo,
        "marca": v.marca,
        "ano": v.ano,
        "categoria": v.categoria,
        "status": v.status,
        "observacoes": v.observacoes,
        "created_at": v.created_at,
    }
