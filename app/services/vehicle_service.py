from __future__ import annotations

import logging
from typing import List, Optional

from sqlalchemy import select, or_

from app.core.database import session_scope
from app.core.utils import is_valid_plate, normalize_plate
from app.models.vehicle import Vehicle

logger = logging.getLogger(__name__)


def _to_dict(v: Vehicle) -> dict:
    return {
        "id": v.id,
        "placa": v.placa,
        "modelo": v.modelo,
        "categoria": v.categoria,
        "status": v.status,
        "observacoes": v.observacoes,
    }


class VehicleService:
    def create(
        self,
        *,
        placa: str,
        modelo: str,
        categoria: str,
        observacoes: str | None,
    ) -> dict:
        placa_n = normalize_plate(placa)
        if not is_valid_plate(placa_n):
            raise ValueError("Placa invalida. Use o padrao ABC-1234 ou ABC1D23.")

        with session_scope() as s:
            v = Vehicle(
                placa=placa_n,
                modelo=modelo.strip(),
                categoria=categoria,
                status="Ativo",
                observacoes=(observacoes or "").strip() or None,
            )
            s.add(v)
            s.flush()
            s.refresh(v)
            logger.info("Veiculo criado: %s", placa_n)
            return _to_dict(v)

    def update(
        self,
        vehicle_id: int,
        *,
        placa: str,
        modelo: str,
        categoria: str,
        observacoes: str | None,
    ) -> None:
        placa_n = normalize_plate(placa)
        if not is_valid_plate(placa_n):
            raise ValueError("Placa invalida. Use o padrao ABC-1234 ou ABC1D23.")

        with session_scope() as s:
            v = s.get(Vehicle, vehicle_id)
            if not v:
                raise ValueError("Veiculo nao encontrado.")
            v.placa = placa_n
            v.modelo = modelo.strip()
            v.categoria = categoria
            v.observacoes = (observacoes or "").strip() or None
            logger.info("Veiculo atualizado: %s", placa_n)

    def delete(self, vehicle_id: int) -> None:
        with session_scope() as s:
            v = s.get(Vehicle, vehicle_id)
            if not v:
                return
            s.delete(v)
            logger.info("Veiculo removido: %s", v.placa)

    def get(self, vehicle_id: int) -> Optional[dict]:
        with session_scope() as s:
            v = s.get(Vehicle, vehicle_id)
            return _to_dict(v) if v else None

    def list(self, search: str = "") -> List[dict]:
        search = (search or "").strip()
        with session_scope() as s:
            stmt = select(Vehicle)
            if search:
                like = f"%{search}%"
                stmt = stmt.where(
                    or_(
                        Vehicle.placa.ilike(like),
                        Vehicle.modelo.ilike(like),
                    )
                )
            stmt = stmt.order_by(Vehicle.placa.asc())
            rows = s.execute(stmt).scalars().all()
            return [_to_dict(v) for v in rows]
