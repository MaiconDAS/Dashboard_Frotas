from __future__ import annotations

import json
import logging

from app.core.database import session_scope
from app.models.setting import Setting

logger = logging.getLogger(__name__)


class CategoryService:
    _KEY = "vehicle_categories"
    _DEFAULT = ["Carga Pesada", "Carga Leve", "Outros"]

    @staticmethod
    def _get_setting(session):
        s = session.query(Setting).filter_by(chave=CategoryService._KEY).first()
        if not s:
            s = Setting(
                chave=CategoryService._KEY,
                valor=json.dumps(CategoryService._DEFAULT),
            )
            session.add(s)
            session.flush()
        return s

    @staticmethod
    def list() -> list[str]:
        with session_scope() as session:
            s = CategoryService._get_setting(session)
            try:
                return json.loads(s.valor)
            except Exception:
                return list(CategoryService._DEFAULT)

    @staticmethod
    def add(name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Nome da categoria nao pode ser vazio.")
        with session_scope() as session:
            s = CategoryService._get_setting(session)
            cats = json.loads(s.valor)
            if name in cats:
                raise ValueError(f"Categoria '{name}' ja existe.")
            cats.append(name)
            s.valor = json.dumps(cats)

    @staticmethod
    def update(old_name: str, new_name: str) -> None:
        old_name = old_name.strip()
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("Nome da categoria nao pode ser vazio.")
        with session_scope() as session:
            s = CategoryService._get_setting(session)
            cats = json.loads(s.valor)
            if old_name not in cats:
                raise ValueError(f"Categoria '{old_name}' nao encontrada.")
            if new_name in cats and new_name != old_name:
                raise ValueError(f"Categoria '{new_name}' ja existe.")
            cats[cats.index(old_name)] = new_name
            s.valor = json.dumps(cats)

    @staticmethod
    def delete(name: str) -> None:
        name = name.strip()
        with session_scope() as session:
            s = CategoryService._get_setting(session)
            cats = json.loads(s.valor)
            if name not in cats:
                raise ValueError(f"Categoria '{name}' nao encontrada.")
            cats.remove(name)
            s.valor = json.dumps(cats)
