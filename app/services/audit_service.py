from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from app.core.database import session_scope
from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    @staticmethod
    def log(
        *,
        username: str,
        acao: str,
        entidade: str,
        entidade_id: int | None,
        descricao: str,
        data_retroativa: datetime | None = None,
    ) -> None:
        with session_scope() as session:
            log = AuditLog(
                usuario=username,
                acao=acao,
                entidade=entidade,
                entidade_id=entidade_id,
                descricao=descricao,
                data_retroativa=data_retroativa,
            )
            session.add(log)
            logger.info("Auditoria: %s por %s (entidade=%s id=%s)", acao, username, entidade, entidade_id)

    @staticmethod
    def list_all(limit: int = 2000) -> List[dict]:
        with session_scope() as session:
            logs = session.query(AuditLog).order_by(AuditLog.data_hora.desc()).limit(limit).all()
            return [
                {
                    "id": l.id,
                    "usuario": l.usuario,
                    "acao": l.acao,
                    "entidade": l.entidade,
                    "entidade_id": l.entidade_id,
                    "descricao": l.descricao,
                    "data_hora": l.data_hora,
                    "data_retroativa": l.data_retroativa,
                }
                for l in logs
            ]
