from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, select, desc, asc

from app.core.database import session_scope
from app.models.activity import Activity
from app.models.vehicle import Vehicle
from app.services.audit_service import AuditService

logger = logging.getLogger(__name__)


@dataclass
class ActivityFilters:
    vehicle_id: Optional[int] = None
    start_dt: Optional[datetime] = None
    end_dt: Optional[datetime] = None
    categoria: Optional[str] = None


def _apply_filters(stmt, f: ActivityFilters):
    if f.vehicle_id:
        stmt = stmt.where(Activity.veiculo_id == f.vehicle_id)
    if f.start_dt:
        stmt = stmt.where(Activity.data_hora >= f.start_dt)
    if f.end_dt:
        stmt = stmt.where(Activity.data_hora <= f.end_dt)
    if f.categoria and f.categoria != "Todas":
        stmt = stmt.where(Vehicle.categoria == f.categoria)
    return stmt


def _activity_to_dict(a: Activity) -> dict:
    return {
        "id": a.id,
        "veiculo_id": a.veiculo_id,
        "data_hora": a.data_hora,
        "quantidade": a.quantidade,
        "observacoes": a.observacoes,
        "created_at": a.created_at,
    }


def _vehicle_to_dict(v: Vehicle) -> dict:
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


class ActivityService:
    def create(
        self,
        *,
        veiculo_id: int,
        data_hora: datetime,
        quantidade: int,
        observacoes: str | None,
        username: str | None = None,
    ) -> dict:
        if quantidade < 0:
            raise ValueError("Quantidade nao pode ser negativa.")

        placa = "?"
        nome = "?"
        with session_scope() as s:
            a = Activity(
                veiculo_id=veiculo_id,
                data_hora=data_hora,
                quantidade=quantidade,
                observacoes=(observacoes or "").strip() or None,
            )
            s.add(a)
            s.flush()
            s.refresh(a)

            v = s.get(Vehicle, veiculo_id)
            if v:
                placa = v.placa
                nome = v.modelo or "?"

            logger.info("Atividade criada (id=%s)", a.id)
            result = _activity_to_dict(a)

        if username:
            agora = datetime.now()
            desc = (
                f"{username} registrou {quantidade} atividade(s) do veiculo {nome} (placa {placa}) "
                f"no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h "
                f"para o dia {data_hora.strftime('%d/%m/%Y')}"
            )
            AuditService.log(
                username=username,
                acao="CREATE",
                entidade="activity",
                entidade_id=result["id"],
                descricao=desc,
                data_retroativa=data_hora,
            )

        return result

    def update(
        self,
        activity_id: int,
        *,
        veiculo_id: int,
        data_hora: datetime,
        quantidade: int,
        observacoes: str | None,
        username: str | None = None,
    ) -> None:
        if quantidade < 0:
            raise ValueError("Quantidade nao pode ser negativa.")

        placa = "?"
        nome = "?"
        old_quantidade = None
        with session_scope() as s:
            a = s.get(Activity, activity_id)
            if not a:
                raise ValueError("Atividade nao encontrada.")

            old_quantidade = a.quantidade

            a.veiculo_id = veiculo_id
            a.data_hora = data_hora
            a.quantidade = quantidade
            a.observacoes = (observacoes or "").strip() or None

            v = s.get(Vehicle, veiculo_id)
            if v:
                placa = v.placa
                nome = v.modelo or "?"

            logger.info("Atividade atualizada (id=%s)", activity_id)

        if username:
            agora = datetime.now()
            desc = (
                f"{username} editou atividade do veiculo {nome} (placa {placa}) "
                f"de {old_quantidade} para {quantidade} atividade(s) "
                f"no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h "
                f"(data retroativa: {data_hora.strftime('%d/%m/%Y')})"
            )
            AuditService.log(
                username=username,
                acao="UPDATE",
                entidade="activity",
                entidade_id=activity_id,
                descricao=desc,
                data_retroativa=data_hora,
            )

    def delete(self, activity_id: int, username: str | None = None) -> None:
        placa = "?"
        nome = "?"
        data_hora = None
        quantidade = None

        with session_scope() as s:
            a = s.get(Activity, activity_id)
            if not a:
                return

            v = s.get(Vehicle, a.veiculo_id)
            if v:
                placa = v.placa
                nome = v.modelo or "?"
            data_hora = a.data_hora
            quantidade = a.quantidade

            s.delete(a)
            logger.info("Atividade removida (id=%s)", activity_id)

        if username and data_hora and quantidade is not None:
            agora = datetime.now()
            desc = (
                f"{username} excluiu {quantidade} atividade(s) do veiculo {nome} (placa {placa}) "
                f"no dia {agora.strftime('%d/%m/%Y')} as {agora.strftime('%H:%M')}h "
                f"(data retroativa: {data_hora.strftime('%d/%m/%Y')})"
            )
            AuditService.log(
                username=username,
                acao="DELETE",
                entidade="activity",
                entidade_id=activity_id,
                descricao=desc,
                data_retroativa=data_hora,
            )

    def get(self, activity_id: int) -> Optional[dict]:
        with session_scope() as s:
            a = s.get(Activity, activity_id)
            return _activity_to_dict(a) if a else None

    def list_all(self, filters: ActivityFilters) -> List[Tuple[dict, dict]]:
        with session_scope() as s:
            stmt = select(Activity, Vehicle).join(Vehicle, Vehicle.id == Activity.veiculo_id)
            stmt = _apply_filters(stmt, filters).order_by(desc(Activity.data_hora))
            rows = list(s.execute(stmt).all())
            return [(_activity_to_dict(a), _vehicle_to_dict(v)) for a, v in rows]

    def list_paginated(
        self,
        filters: ActivityFilters,
        *,
        page: int,
        page_size: int,
        order_by: str = "data_hora",
        order_desc: bool = True,
    ) -> Tuple[List[Tuple[dict, dict]], int]:
        page = max(1, page)
        page_size = max(10, min(200, page_size))

        with session_scope() as s:
            base = select(Activity, Vehicle).join(Vehicle, Vehicle.id == Activity.veiculo_id)
            base = _apply_filters(base, filters)

            count_base = select(func.count()).select_from(Activity).join(
                Vehicle, Vehicle.id == Activity.veiculo_id
            )
            count_stmt = _apply_filters(count_base, filters)
            total = int(s.execute(count_stmt).scalar_one())

            if order_by == "veiculo":
                order_col = Vehicle.placa
            else:
                order_col = Activity.data_hora

            order_expr = desc(order_col) if order_desc else asc(order_col)
            stmt = base.order_by(order_expr).offset((page - 1) * page_size).limit(page_size)
            rows = list(s.execute(stmt).all())
            return [(_activity_to_dict(a), _vehicle_to_dict(v)) for a, v in rows], total

    def kpis(self, filters: ActivityFilters) -> dict:
        with session_scope() as s:
            base = select(Activity).join(Vehicle, Vehicle.id == Activity.veiculo_id)
            base = _apply_filters(base, filters)
            sub = base.subquery()

            total_ativ = int(s.execute(select(func.count()).select_from(sub)).scalar_one())
            qtd_expr = func.coalesce(func.sum(sub.c.quantidade), 0)
            qtd_total = int(s.execute(select(qtd_expr)).scalar_one())

            top_stmt = select(Vehicle.modelo, func.count(Activity.id).label("qtd")).select_from(
                Activity
            ).join(Vehicle, Vehicle.id == Activity.veiculo_id)
            top_stmt = _apply_filters(top_stmt, filters)
            top_stmt = top_stmt.group_by(Vehicle.modelo).order_by(desc("qtd")).limit(5)
            top = list(s.execute(top_stmt).all())

            dia_stmt = select(func.date(Activity.data_hora), func.sum(Activity.quantidade)).select_from(
                Activity
            ).join(Vehicle, Vehicle.id == Activity.veiculo_id)
            dia_stmt = _apply_filters(dia_stmt, filters)
            dia_stmt = dia_stmt.group_by(func.date(Activity.data_hora)).order_by(
                asc(func.date(Activity.data_hora))
            )
            por_dia = list(s.execute(dia_stmt).all())

            return {
                "total_atividades": total_ativ,
                "quantidade_total": qtd_total,
                "top_veiculos": [(nome, int(q)) for nome, q in top],
                "por_dia": [(str(d), int(q)) for d, q in por_dia],
            }