from __future__ import annotations

import hashlib
import logging
import secrets
from typing import Optional

from app.core.database import session_scope
from app.models.admin import Admin
from app.models.setting import Setting

logger = logging.getLogger(__name__)


class AdminService:
    _MASTER_KEY = "master_password_hash"

    @staticmethod
    def _hash_password(password: str, salt: bytes | None = None) -> tuple[str, bytes]:
        if salt is None:
            salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return key.hex(), salt

    @staticmethod
    def _verify_password(password: str, stored_hash: str, salt: bytes) -> bool:
        key, _ = AdminService._hash_password(password, salt)
        return secrets.compare_digest(key, stored_hash)

    @staticmethod
    def get_master_password_hash() -> str | None:
        with session_scope() as session:
            s = session.query(Setting).filter_by(chave=AdminService._MASTER_KEY).first()
            return s.valor if s else None

    @staticmethod
    def set_master_password(password: str) -> None:
        hash_hex, salt = AdminService._hash_password(password)
        stored = f"{hash_hex}:{salt.hex()}"
        with session_scope() as session:
            s = session.query(Setting).filter_by(chave=AdminService._MASTER_KEY).first()
            if s:
                s.valor = stored
            else:
                session.add(Setting(chave=AdminService._MASTER_KEY, valor=stored))

    @staticmethod
    def validate_master_password(password: str) -> bool:
        stored = AdminService.get_master_password_hash()
        if not stored:
            return False
        try:
            hash_hex, salt_hex = stored.split(":")
            return AdminService._verify_password(password, hash_hex, bytes.fromhex(salt_hex))
        except Exception:
            return False

    @staticmethod
    def create_admin(*, username: str, password: str, nome_completo: str, is_master: bool = False) -> dict:
        with session_scope() as session:
            existing = session.query(Admin).filter_by(username=username).first()
            if existing:
                raise ValueError(f"Usuario '{username}' ja existe.")

            hash_hex, salt = AdminService._hash_password(password)
            admin = Admin(
                username=username,
                password_hash=f"{hash_hex}:{salt.hex()}",
                nome_completo=nome_completo,
                is_master=int(is_master),
                is_active=1,
            )
            session.add(admin)
            session.flush()
            session.refresh(admin)
            return _to_dict(admin)

    @staticmethod
    def authenticate(username: str, password: str) -> dict | None:
        with session_scope() as session:
            admin = session.query(Admin).filter_by(username=username, is_active=1).first()
            if not admin:
                return None
            try:
                hash_hex, salt_hex = admin.password_hash.split(":")
                if AdminService._verify_password(password, hash_hex, bytes.fromhex(salt_hex)):
                    return _to_dict(admin)
            except Exception:
                logger.exception("Falha na verificacao de senha")
            return None

    @staticmethod
    def get_all() -> list[dict]:
        with session_scope() as session:
            admins = session.query(Admin).order_by(Admin.id).all()
            return [_to_dict(a) for a in admins]

    @staticmethod
    def update_admin(admin_id: int, *, nome_completo: str, username: str, new_password: str | None = None) -> None:
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                raise ValueError("Administrador nao encontrado.")

            if admin.username != username:
                existing = session.query(Admin).filter_by(username=username).first()
                if existing:
                    raise ValueError(f"Usuario '{username}' ja existe.")

            admin.nome_completo = nome_completo
            admin.username = username

            if new_password:
                hash_hex, salt = AdminService._hash_password(new_password)
                admin.password_hash = f"{hash_hex}:{salt.hex()}"

    @staticmethod
    def deactivate_admin(admin_id: int) -> bool:
        """Soft delete: marca como inativo."""
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                return False
            admin.is_active = 0
            return True

    @staticmethod
    def hard_delete_admin(admin_id: int) -> bool:
        """Hard delete: remove fisicamente do banco. Login fica disponivel novamente."""
        with session_scope() as session:
            admin = session.get(Admin, admin_id)
            if not admin:
                return False
            session.delete(admin)
            return True


def _to_dict(admin: Admin) -> dict:
    return {
        "id": admin.id,
        "username": admin.username,
        "nome_completo": admin.nome_completo,
        "is_master": bool(admin.is_master),
        "is_active": bool(admin.is_active),
        "created_at": admin.created_at,
    }
