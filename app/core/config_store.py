from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from app.core.paths import APP_NAME, get_config_path

try:
    from cryptography.fernet import Fernet
except Exception:  # pragma: no cover
    Fernet = None  # type: ignore


def _derive_key() -> bytes:
    """
    Chave derivada de informações locais (não é criptografia forte),
    suficiente para "pelo menos ofuscar" como exigido.
    """
    machine = os.environ.get("COMPUTERNAME", "unknown")
    user = os.environ.get("USERNAME", "unknown")
    seed = f"{APP_NAME}|{machine}|{user}|v1".encode("utf-8")
    digest = hashlib.sha256(seed).digest()
    return base64.urlsafe_b64encode(digest)


def _encrypt(text: str) -> str:
    if not text:
        return ""
    raw = text.encode("utf-8")
    if Fernet is not None:
        f = Fernet(_derive_key())
        return "f:" + f.encrypt(raw).decode("utf-8")
    # fallback (ofuscação simples)
    x = bytes(b ^ 0x5A for b in raw)
    return "x:" + base64.urlsafe_b64encode(x).decode("utf-8")


def _decrypt(value: str) -> str:
    if not value:
        return ""
    if value.startswith("f:") and Fernet is not None:
        f = Fernet(_derive_key())
        return f.decrypt(value[2:].encode("utf-8")).decode("utf-8")
    if value.startswith("x:"):
        x = base64.urlsafe_b64decode(value[2:].encode("utf-8"))
        raw = bytes(b ^ 0x5A for b in x)
        return raw.decode("utf-8")
    # compat
    return value


@dataclass
class AppConfig:
    company_name: str = "Loja de Materiais de Construção"
    logo_path: str = ""
    theme: str = "dark"  # dark|light

    smtp_host: str = ""
    smtp_port: int = 587
    sender_email: str = ""
    sender_password_enc: str = ""  # armazenado ofuscado
    manager_email: str = ""
    use_tls: bool = True
    use_ssl: bool = False

    weekly_enabled: bool = False
    last_weekly_sent_end_iso: str = ""  # YYYY-MM-DD do último domingo enviado

    @property
    def sender_password(self) -> str:
        return _decrypt(self.sender_password_enc)

    @sender_password.setter
    def sender_password(self, value: str) -> None:
        self.sender_password_enc = _encrypt(value)


class ConfigStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path or get_config_path()
        self._config = AppConfig()

    def load(self) -> AppConfig:
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self._config = AppConfig(**{**asdict(AppConfig()), **data})
        return self._config

    def save(self, config: AppConfig) -> None:
        self._config = config
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(asdict(config), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get(self) -> AppConfig:
        return self._config

    def set_last_weekly_sent_end(self, end_date: datetime) -> None:
        cfg = self.get()
        cfg.last_weekly_sent_end_iso = end_date.strftime("%Y-%m-%d")
        self.save(cfg)

